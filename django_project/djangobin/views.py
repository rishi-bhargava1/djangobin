from django.shortcuts import HttpResponse, render
import datetime
from django.conf import settings

# Create your views here.


def index(request):
    return HttpResponse('<p>Index Page</p>')


def profile(request, username):
    html = f"<html><body>Profile Page of: {username}</body></html>"
    return HttpResponse(html)