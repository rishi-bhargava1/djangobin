from django import forms
from django.core.exceptions import ValidationError
from .models import Language


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data['name']
        if name == 'djangobin' or name == 'DJANGOBIN':
            raise ValidationError("name can't be {}.".format(name))

        # Always return the data
        return name

    def clean_slug(self):
        return self.cleaned_data['slug'].lower()

    def clean(self):
        cleaned_data = super(LanguageForm, self).clean()
        slug = cleaned_data.get('slug')
        mime = cleaned_data.get('mime')

        if slug == mime:
            raise ValidationError("Slug and MIME shouldn't be same.")

        # Always return the data
        return cleaned_data