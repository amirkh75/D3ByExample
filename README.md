# D3ByExample
projects from Django 3 by example.


Chapter 1: Building a Blog Application


Designing models and generating model migrations
Creating an administration site
Working with QuerySets and managers
Duilding views, templates, and URLs
Adding pagination to list views
Using Django's class-base views

I decided to use docker and use "Dockerizing Django with Postgres, Gunicorn, and Nginx" from https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/

And I choes use custom user that extend AbstractBaseUser base on "Creating a Custom User Model in Django" from https://testdriven.io/blog/django-custom-user-model/

Also  i add profile model that use custom user model and it creates authomatically when user created with django signals.


Used bootstrap 5 for templates.


Chapter 2: Enhancing Your Blog With Advanced Features


Sending emails with Django
Creating forms and handling them in views
Creating form for models
Integrating third-party applications
Building complex QuerySets

I used gmail free smtp server. todo move some securety code to .env files

I also change and use forms in better way.

some chnage on comment model

I'm not so sure about my database design , becuse it has so meny fks.


Chapter 3: Extending Your Blog Application


Creating custom template teags and filters
Adding a sitemap and post feed
Implementing full-text search with PostgreSQL


made me to create a seprate dockerfile in name pg-Dockerfile and load-extensions.sh for " extension pg_trgm", for trgm text search.


