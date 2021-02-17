from django.conf.urls import url
from . import views

app_name = 'djangobin'

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^user/(?P<username>[A-Za-z0-9]+)/$', views.profile, name='profile'),
]