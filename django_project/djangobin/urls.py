from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.shortcuts import reverse
from django.urls import reverse_lazy
from . import views

app_name = 'djangobin'

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^contact/$', views.contact, name="contact"),
    url('^download/(?P<snippet_slug>[\d]+)/$', views.download_snippet, name='download_snippet'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^user/(?P<username>[A-Za-z0-9]+)/$', views.profile, name='profile'),
    url('^raw/(?P<snippet_slug>[\d]+)/$', views.raw_snippet, name='raw_snippet'),
    url('^(?P<snippet_slug>[\d]+)/$', views.snippet_detail, name='snippet_detail'),
    url('^trending/$', views.trending_snippets, name='trending_snippets'),
    url('^trending/(?P<language_slug>[\w]+)/$', views.trending_snippets, name='trending_snippets'),
    url('^tag/(?P<tag_slug>[\w-]+)/$', views.tag_list, name='tag_list'),
    url(r'^userdetails/$', views.user_details, name='user_details'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r"^activate/"
        r"(?P<uidb64>[0-9A-Za-z_\-]+)/"
        r"(?P<token>[0-9A-Za-z]{1,13}"
        r"-[0-9A-Za-z]{1,20})/$",
        views.activate_account, name='activate'),
    url(r'^password-reset/$',
        auth_views.PasswordResetView.as_view(
                                             template_name="djangobin/password_reset.html",
                                             email_template_name="djangobin/email/password_reset_email.txt",
                                             subject_template_name="djangobin/email/password_reset_subject.txt",
                                             success_url=reverse_lazy('djangobin:password_reset_done')
                                            ), name="password_reset"),
    url('^password-reset-done/$',
        auth_views.PasswordResetDoneView.as_view(
                                                 template_name='djangobin/password_reset_done.html',
                                                ), name="password_reset_done"),
    url(r'^password-confirm/'
        r'(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}'
        r'-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
                                                    template_name='djangobin/password_reset_confirm.html',
                                                    success_url=reverse_lazy('djangobin:password_reset_complete')
                                                   ), name="password_reset_confirm"),
    url(r'password-reset-complete/$',
        auth_views.PasswordResetCompleteView.as_view(
                                                     template_name='djangobin/password_reset_complete.html'
                                                    ), name="password_reset_complete"),
    url(r'^password-change/$', auth_views.PasswordChangeView.as_view(
                                                                     template_name='djangobin/password_change.html',
                                                                     success_url=reverse_lazy('djangobin:password_change_done')
                                                                    ), name="password_change"),
    url(r'^password-change-done/$', auth_views.PasswordChangeDoneView.as_view(
                                                                              template_name='djangobin/password_change_done.html'
                                                                             ), name="password_change_done"),
]