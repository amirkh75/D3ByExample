Chapter 4, 5 and 6 

A social application (image sharing platform), which users are able to bookmark any image on the internet and share it with others.

Users can like/unlike, follow and see activity of his/her following users.

Chapter 4 topics:

1.Using the Django authentication framework.
2.Creating user registration views.
3.Extending the user model with a custom profile model.
4.Adding social authentication with Python Socail Auth.

I also add docker to the project on my own{ [some help](https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/)
    1.create virtual env, install django and start django by create config(django-admin.py startproject).

    2.add Dockerfile, requirements.txt, docker-compose.yml , .env.dev and move allowed hosts, security key and Debug to env.dev for just development uses.
    -use docker-compose to manage dockerfile.

    3.docker-compose build and up -d

    4. use postgres as database:
        add service-db to dockerfile,
        env, DATABASE(setting.py), requirements.txt and
        postgresql-dev gcc python3-dev musl-dev to docker-compose.
        and then  to verify that Postgres is healthy before applying the migrations and running the Django development server add entrypoint.sh.

    5.add Gunicorn, a production-grade WSGI server:
        add to requirements
        since we use it just for production we create docker-compose.prod.yml and .env.prod and .env.prod.db for product mode envs.

    6.production Dockerfile:
        add entrypoint.prod.sh, and Dockerfile.prod, .flake8

    7.add Nginx into the mix to act as a reverse proxy for Gunicorn to handle client requests as well as serve up static files.
      create nginx directory(dockerfile and nginx.conf), and add docker-compose.prod.

    8.load Static Files and Media Files with nginx on production mode.

}

start chapter 4 by creating the account app.

With this command : docker-compose exec web python manage.py startapp account
use django user model(django.contrib.auth) and authentication system.
write login.

Using Django authentication views.resetting password with email(on consol).

User registration and user profiles(Extending the user model).add picture with pillow.


Using the messages framework
    The messages framework is located at django.contrib.messages and is included
    in the default INSTALLED_APPS list of the settings.py file when you create new
    projects using python manage.py startproject. You will note that your settings
    file contains a middleware named django.contrib.messages.middleware.
    MessageMiddleware in the MIDDLEWARE settings.
    they are displayed in the next request from the user.

Building a custom authentication backend.


Adding social authentication to your site. add 0.0.0.0:8000 to runserver_plus add twitter and google authentication.


Chapter 5 topics:

Building a bookmarklet with jQuery
A bookmarklet is a bookmark stored in a web browser that contains JavaScript
code to extend the browser's functionality. When you click on the bookmark, the
JavaScript code is executed on the website being displayed in the browser. This is
very useful for building tools that interact with other websites.

Now let's add AJAX actions to your application. AJAX comes from Asynchronous
JavaScript and XML, encompassing a group of techniques to make asynchronous
HTTP requests.

When you submit forms, you can use the {% csrf_token %}
template tag to send the token along with the form. However, it is a bit inconvenient
for AJAX requests to pass the CSRF token as POST data with every POST request.
Therefore, Django allows you to set a custom X-CSRFToken header in your AJAX
requests with the value of the CSRF token. This enables you to set up jQuery or any
other JavaScript library to automatically set the X-CSRFToken header in every request.

add images app and jquery and especially ajax to this project for asynchronous post requests.



Chapter 6 topics:

Building a follow system.

Building an AJAX view to follow users.

Building a generic activity stream application (add actions app).

Adding generic relations to your models.

Optimizing QuerySets that involve related objects.

Using signals for denormalizing counts.

Using Redis for storing item views

