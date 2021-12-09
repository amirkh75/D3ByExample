from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse


def home(request):
    context = {'segment': 'Home'}

    html_template = loader.get_template('pages/home.html')
    return HttpResponse(html_template.render(context, request))