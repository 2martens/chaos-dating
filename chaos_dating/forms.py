# coding=utf-8
from django import forms

from chaos_dating.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gender', 'wishes']
        localized_fields = ['gender', 'wishes']
