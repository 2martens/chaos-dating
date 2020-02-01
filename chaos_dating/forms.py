# coding=utf-8
from django import forms

from chaos_dating.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['pronoun', 'gender', 'wishes']
        localized_fields = ['pronoun', 'gender', 'wishes']
