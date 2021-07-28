from django.shortcuts import HttpResponse, render, redirect
import datetime
from django.conf import settings
from .forms import LanguageForm

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


def add_lang(request):
    if request.POST:
        f = LanguageForm(request.POST)
        if f.is_valid():
            lang = f.save()
            return redirect('djangobin:add_lang')

    else:
        f = LanguageForm()

    return render(request, 'djangobin/add_lang.html', {'form': f} )