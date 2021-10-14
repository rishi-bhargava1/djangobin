import datetime
# from django.conf import settings
from .forms import SnippetForm, ContactForm, LoginForm, CreateUserForm
from .models import Snippet, Language, Tag
from .utils import paginate_result
from django.core.mail import mail_admins
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import (HttpResponse, render, redirect, get_object_or_404, get_list_or_404 , reverse)
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode

# Create your views here.

# 16284283111150227
def index(request):
    if request.POST:
        f = SnippetForm(request.POST)
        print("============Check validity =============")
        if f.is_valid():
            # request pass to *args of overridden save() method in forms.py.
            snippet = f.save(request)
            messages.add_message(request, messages.INFO, 'Snippet saved.')
            return redirect(reverse('djangobin:snippet_detail', args=[snippet.slug]))
            # return redirect(reverse('djangobin:index'))

    else:
        f = SnippetForm()
        print("============FirstForm / Not valid==========")

    return render(request, 'djangobin/index.html', {'form': f})


def snippet_detail(request, snippet_slug):
    print("=============== Snippet Url", reverse('djangobin:snippet_detail', args=[snippet_slug]))
    snippet = get_object_or_404(Snippet, slug=snippet_slug)
    snippet.hits += 1
    snippet.save()
    return render(request, 'djangobin/snippet_detail.html', {'snippet': snippet})


def trending_snippets(request, language_slug=''):
    lang = None
    # To get object manager
    snippets = Snippet.objects

    if language_slug:
        lang = get_object_or_404(Language, slug=language_slug)
        snippet_list = snippets.filter(language__slug=language_slug, exposure='public').order_by("-hits")
    else:
        snippet_list = get_list_or_404(snippets.filter(exposure='public').order_by('-hits'))

    snippets = paginate_result(request, snippet_list, 5)
    return render(request, 'djangobin/trending.html', {'snippets': snippets, 'lang': lang})


def tag_list(request, tag_slug):
    t = get_object_or_404(Tag, name=tag_slug)
    snippet_list = get_list_or_404(t.snippet_set)
    snippets = paginate_result(request, snippet_list, 5)
    return render(request, 'djangobin/tag_list.html', {'snippets': snippets, 'tag': t})


def profile(request, username):
    html = f"<html><body>Profile Page of: {username}</body></html>"
    return HttpResponse(html)


def download_snippet(request, snippet_slug):
    snippet = get_object_or_404(Snippet, slug=snippet_slug)
    file_extension = snippet.language.file_extension
    filename = snippet.slug + file_extension
    res = HttpResponse(snippet.original_code)
    res['content-disposition'] = f'attachment; filename= {filename};'
    return res


def raw_snippet(request, snippet_slug):
    snippet = get_object_or_404(Snippet, slug=snippet_slug)
    return HttpResponse(snippet.original_code, content_type=snippet.language.mime)


def contact(request):
    if request.method == 'POST':
        f = ContactForm(request.POST)

        if f.is_valid():
            name = f.cleaned_data['name']
            email = f.cleaned_data['email']
            subject = "You have a new Feedback from {}:<{}>".format(name, email)

            message = "Purpose: {}\n\nDate: {}\n\nMessage:\n\n {}".format(
                # 'f' is a object and 'purpose_choices' tuple is a class variable of ContactForm class.
                dict(f.purpose_choices).get(f.cleaned_data['purpose']),
                datetime.datetime.now(),
                f.cleaned_data['message']
            )

            mail_admins(subject, message)
            messages.add_message(request, messages.INFO, 'Thanks for submitting your feedback.')

            return redirect('djangobin:contact')

    else:
        f = ContactForm()

    return render(request, 'djangobin/contact.html', {'form': f})


def login(request):
    if request.user.is_authenticated:
        return redirect('djangobin:profile', request.user.username)

    if request.method == 'POST':

        f = LoginForm(request.POST)
        if f.is_valid():

            user = User.objects.filter(email=f.cleaned_data['email'])

            if user:
                user = auth.authenticate(
                                         username=user[0].username,
                                         password=f.cleaned_data['password'],
                                        )

                if user:
                    auth.login(request, user)
                    return redirect(request.GET.get('next') or 'djangobin:profile', user.username)

            messages.add_message(request, messages.INFO, 'Invalid email/password.')
            return redirect('djangobin:login')

    else:
        f = LoginForm()

    return render(request, 'djangobin/login.html', {'form': f})


def logout(request):
    if not request.user.is_authenticated:
        return HttpResponse("<h4>You are not logged in.</h4><p><a href='/login/'>Click here</a> to login.</p>")
    auth.logout(request)
    return render(request,'djangobin/logout.html')


@login_required
def user_details(request):
    user = get_object_or_404(User, id=request.user.id)
    return render(request, 'djangobin/user_details.html', {'user': user})


def signup(request):
    if request.method == 'POST':
        f = CreateUserForm(request.POST)
        if f.is_valid():
            f.save(request)
            messages.success(request, 'Account created successfully. Check email to verify the account.')
            return redirect('djangobin:signup')

    else:
        f = CreateUserForm()

    return render(request, 'djangobin/signup.html', {'form': f})


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.add_message(request, messages.INFO, 'Account activated. Please login.')
    else:
        messages.add_message(request, messages.INFO, 'Link Expired. Contact admin to activate your account.')

    return redirect('djangobin:login')
