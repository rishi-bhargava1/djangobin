from .models import Snippet, Tag
from .utils import get_current_user
from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class SnippetForm(forms.ModelForm):
    snippet_tags = forms.CharField(required=False, help_text="'This field only contains "
                                                             "alphabets and tags separate by comma(,) .",
                                   widget=forms.TextInput(attrs={
                                       'placeholder': 'Enter tags (optional)'},
                                   ))

    class Meta:
        model = Snippet
        fields = ('original_code', 'language', 'expiration', 'exposure', 'title')
        widgets = {
            'original_code': forms.Textarea(attrs={'rows': '25', 'cols': '100', 'spellcheck': 'false'}),
            'language': forms.Select(attrs={'size': '4'}),
            'title': forms.TextInput(attrs={'placeholder': 'Enter Title (optional)'}),
        }

    def clean_snippet_tags(self):
        tags = self.cleaned_data['snippet_tags']
        f_tags = []

        for tag in tags.split(','):
            tag = tag.strip().lower()
            if not tag.isalpha():
                raise ValidationError("Tag name considers only alphabets!")
            f_tags.append(tag)

        return f_tags

    def save(self, *args, commit=False):
        # Get the Snippet object like dummy object, without saving it into the database by commit=False.
        snippet = super(SnippetForm, self).save(commit=False)

        # Here args[0] is 'request' object from index view.
        snippet.user = get_current_user(args[0])
        snippet.save()  # This is save() method of models.Model class.
        print("============ Snippet Saved==========")

        tag_list = self.cleaned_data['snippet_tags']
        if tag_list:
            for tag in tag_list:
                t = Tag.objects.get_or_create(name=tag)

                # get_or_create() returns tuple of (object, created_bool)
                snippet.tags.add(t[0])

        return snippet


class ContactForm(forms.Form):
    BUG = 'b'
    FEEDBACK = 'fb'
    NEW_FEATURE = 'nf'
    OTHER = 'o'
    purpose_choices = (
        (FEEDBACK, 'Feedback'),
        (NEW_FEATURE, 'Feature Request'),
        (BUG, 'Bug'),
        (OTHER, 'Other'),
    )

    name = forms.CharField()
    email = forms.EmailField()
    purpose = forms.ChoiceField(choices=purpose_choices)
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}))


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise ValidationError("This field is required.")
        if User.objects.filter(email=self.cleaned_data['email']).count():
            raise ValidationError("Email is taken.")
        return self.cleaned_data['email']

    def save(self, *args, commit=False):
        # Get the User object like dummy object, without saving it into the database by commit=False.

        # Here args[0] is 'request' object from signup view.
        request = args[0]
        user = super(CreateUserForm, self).save(commit=False)
        user.is_active = False
        user.save()

        context = {
            # 'from_email': settings.DEFAULT_FROM_EMAIL,
            'request': request,
            'protocol': request.scheme,
            'username': self.cleaned_data.get('username'),
            'domain': request.META['HTTP_HOST'],
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': default_token_generator.make_token(user),
        }
        print("========Type=========", type(context['uid']), context['uid'])

        subject = render_to_string('djangobin/email/activation_subject.txt', context)
        email = render_to_string('djangobin/email/activation_email.txt', context)

        send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email])

        return user