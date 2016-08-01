import random, string

from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

class LinkManager(models.Manager):
    def find_or_create(self, base_url):
        result = self.get_queryset().filter(base_url = base_url)
        if result.exists():
            link = result.first()
        else:
            link = self.model(base_url = base_url)
            link.generate_short_string()
            link.save()
        return link

    def find_by_short_url(self, short_url):
        short_string = short_url.replace(settings.DOMAIN, "")
        result = self.get_queryset().filter(short_string = short_string)
        if result.exists():
            return result.first()
        else:
            return None

class Link(models.Model):
    base_url = models.CharField('Base URL', max_length=256, unique=True)
    short_string = models.CharField(max_length=30, unique=True)

    objects = LinkManager()

    def __str__(self):
        return str({'id': self.id, 'short_url': self.short_url()})

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Link, self).save(*args, **kwargs)

    def short_url(self):
        return "%s%s" % (settings.DOMAIN, self.short_string)

    def generate_short_string(self, length=6, charset=string.ascii_letters + string.digits):
        randomize = lambda: ''.join(random.SystemRandom().choice(charset) for i in range(length))
        rand_str = randomize()
        while Link.objects.filter(short_string = rand_str).exists():
            rand_str = randomize()
        self.short_string = rand_str
        return self.short_string
