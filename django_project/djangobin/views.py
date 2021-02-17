from django.shortcuts import HttpResponse, render
import datetime
from django.conf import settings

# Create your views here.


def index(request):
    return HttpResponse('<p>Index Page</p>')


def trending_snippets(request, language_slug=''):
    return HttpResponse("trending {} snippets".format(language_slug if language_slug else ""))


def snippet_detail(request, snippet_slug):
    return HttpResponse('viewing snippet #{}'.format(snippet_slug))


def tag_list(request, tag):
    return HttpResponse('viewing tag #{}'.format(tag))


def profile(request, username):
    html = f"<html><body>Profile Page of: {username}</body></html>"
    return HttpResponse(html)