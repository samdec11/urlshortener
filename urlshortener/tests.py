import sure
from sure import expect
from faker import Faker

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.urlresolvers import reverse

from .models import Link, LinkManager

class LinkModelTests(TestCase):
    def test_url_uniqueness(self):
        """
        Saving a Link with a duplicate short_string or base_url should
        raise a ValidationError.
        """
        base = Faker().uri()
        short = Faker().slug()
        link1 = Link(base_url = base, short_string = short)
        link1.save()
        link2 = Link(base_url = base, short_string = short)
        expect(link2.save).when.called.to.throw(
            ValidationError,
            {
                'short_string': ['Link with this Short URL already exists.'],
                'base_url':  ['Link with this Base URL already exists.']
            }
        )

    def test_generate_short_string_sets_short_string(self):
        """
        Calling `generate_short_string` on a Link should set the value of
        the Link's short_string.
        """
        link = Link(base_url = Faker().uri())
        len(link.short_string).should.equal(0)
        link.generate_short_string()
        len(link.short_string).should.be.greater_than(0)

    def test_generate_short_string_returns_unique_value(self):
        """
        The short_string generated should be unique.
        """
        link = Link(base_url = Faker().uri())
        link.generate_short_string()
        (Link.objects.filter(short_string = link.short_string).exists()).should.equal(False)

    def test_find_or_create_with_existing_url(self):
        """
        `find_or_create` should return the existing Link record if one exists that matches
        the passed-in base_url.
        """
        base = Faker().uri()
        short = Faker().slug()
        link = Link.objects.create(base_url = base, short_string = short)
        link2 = Link.objects.find_or_create(base)
        link.id.should.equal(link2.id)

    def test_find_or_create_with_new_url(self):
        """
        `find_or_create` should create a new Link, generate a short_string for it, and
        save it, returning the new Link if a record does not exist with the passed-in
        base_url.
        """
        base = Faker().uri()
        Link.objects.filter(base_url = base).exists().should.equal(False)
        link = Link.objects.find_or_create(base)
        link.id.should_not.equal(None)

class IndexViewTests(TestCase):
    def test_index_view_as_get(self):
        """
        The index should contain the "URL Shortener" header.
        """
        response = self.client.get(reverse('urlshortener:index'))
        response.status_code.should.equal(200)
        self.assertContains(response, 'URL Shortener')

    def test_index_as_post(self):
        """
        There should be text displaying the short URL for the entry.
        """
        response = self.client.post(reverse('urlshortener:index'), {'url': Faker().uri()})
        self.assertContains(response, 'The short URL for this link is')

class RedirectViewTests(TestCase):
    def test_redirect_view_with_unknown_short_url(self):
        """
        The redirect action should render a 404 when a Link is not found.
        """
        response = self.client.get(reverse('urlshortener:redirect', args=('bloop',)))
        response.status_code.should.equal(404)

    def test_redirect_view_with_known_short_url(self):
        """
        The redirect action should redirect to the base_url of the found Link.
        """
        link = Link.objects.find_or_create(base_url = Faker().uri())
        response = self.client.get(reverse('urlshortener:redirect', args=(link.short_string,)))
        response.status_code.should.equal(302)
        response.url.should.equal(link.base_url)
