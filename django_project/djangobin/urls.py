from django.conf.urls import url
from . import views

app_name = 'djangobin'

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^user/(?P<username>[A-Za-z0-9]+)/$', views.profile, name='profile'),
    url('^trending/$', views.trending_snippets, name='trending_snippets'),
    url('^trending/(?P<language_slug>[\w]+)/$', views.trending_snippets, name='trending_snippets'),
    url('^(?P<snippet_slug>[\d]+)/$', views.snippet_detail, name='snippet_detail'),
    url('^tag/(?P<tag>[\w-]+)/$', views.tag_list, name='tag_list'),
    url('^add-lang/$', views.add_lang, name='add_lang'),
]