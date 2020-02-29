# coding=utf-8
from gettext import gettext as _

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User
from django.urls import reverse

from chaos_dating import models
from chaos_dating.models import Profile


class FilterForm(forms.Form):
    wishes = forms.ModelMultipleChoiceField(queryset=models.Wish.objects.all(), required=False)
    gender = forms.ModelMultipleChoiceField(queryset=models.Gender.objects.all(), required=False)
    

class UserForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            'Raw passwords are not stored, so there is no way to see the '
            'password, but you can change the password using '
            '<a href="{}">this form</a>.'
        ),
    )
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        field_classes = {'username': UsernameField}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format(reverse('password_change'))
    
    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial.get('password')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['pronoun', 'gender', 'wishes']
        localized_fields = ['pronoun', 'gender', 'wishes']
