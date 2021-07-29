from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
import datetime
from django.conf import settings
from .forms import LanguageForm
from django.contrib import messages
from .models import Language

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
            messages.add_message(request, messages.INFO, 'Language saved.')
            return redirect('djangobin:add_lang')

    else:
        f = LanguageForm()

    return render(request, 'djangobin/add_lang.html', {'form': f})


def update_lang(request, lang_slug):
    l = get_object_or_404(Language, slug__iexact=lang_slug)
    if request.POST:
        f = LanguageForm(request.POST, instance=l)
        if f.is_valid():
            lang = f.save()
            messages.add_message(request, messages.INFO, 'Language Updated.')
            return redirect('djangobin:update_lang', lang.slug)

    else:
        f = LanguageForm(instance=l)

    return render(request, 'djangobin/update_lang.html', {'form': f} )