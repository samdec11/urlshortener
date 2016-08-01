# URL Shortener

### Summary
When a user visits the site, she is presented with a form. She can enter the URL she would like to shorten, and the system will automatically generate a short URL for her to copy.

The long URL is stored as the `base_url` of a `Link` instance. When the form is submitted, the `LinkManager` runs `find_or_create`, searching for a `Link` that already exists with the entered `base_url`. If one exists, it will be returned and the user will see the `short_url`, which is a concatenation of the domain (`settings.DOMAIN`) and the randomly-generated `short_string`. If one does not exist, a new one will be created with this `base_url` and a `short_string` will be randomly generated in `generate_short_string`.

When a user navigates to a `short_url`, the `redirect` view will search for a `Link` that exists with a matching `short_string` and redirect to its `base_url` if it exists, rendering a 404 if it does not.

An admin is able to log in and see the entire list of `Link`s that have been created.

### Running locally
###### This app was built using Django 1.9.8 and Python 3.5.2. Mac OSX provides support for Python 2 and 3, naming all Python 3 commands as `python3` and Python 2 as `python`. For the purposes of this documentation, I will say `python` in the places where I used `python3`.

##### Packages Needed: [sure](https://github.com/gabrielfalcao/sure), [faker](https://github.com/joke2k/faker)

* Clone the repo and `cd` into the directory.
* I've checked the sqlite file into VC, so you shouldn't need to run migrations, but if you do, run `python manage.py migrate`.
* You can create an admin user with `python manage.py createsuperuser`.
* I have the DOMAIN constant in settings.py set to "http://localhost:8000". To run the local server with this configuration, run `python manage.py runserver localhost:8000`. In a browser, go to localhost:8000 to use the site.
* You can also log in as the admin user you created at /admin to see the list of `Link`s in the database.
* You can run tests with `python manage.py test urlshortener`.
