# coding=utf-8
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import FileField
from django.urls import reverse
from django.utils.translation import gettext as _
from django_select2.forms import Select2MultipleWidget
from django_select2.forms import Select2Widget

from chaos_dating import models


class FilterForm(forms.Form):
    widget = Select2MultipleWidget(attrs={
        'data-dropdown-auto-width': 'true',
    })
    wishes = forms.ModelMultipleChoiceField(queryset=models.Wish.objects.all(), required=False,
                                            widget=widget)
    gender = forms.ModelMultipleChoiceField(queryset=models.Gender.objects.all(), required=False,
                                            widget=widget)
    SORT_CHOICES = (
        ('user__username', _('Username')),
        ('age', _('Age')),
    )
    order_by = forms.ChoiceField(choices=SORT_CHOICES, required=False)
    SORT_ORDER = (
        ('+', _('Ascending')),
        ('-', _('Descending'))
    )
    order_direction = forms.ChoiceField(choices=SORT_ORDER, required=False)


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
        model = models.Profile
        widget = Select2Widget(attrs={
            'data-dropdown-auto-width': 'true',
            'data-tags': 'true'
        })
        fields = ['age', 'pronoun', 'gender', 'wishes']
        localized_fields = ['age', 'pronoun', 'gender', 'wishes']
        widgets = {
            'pronoun': widget,
            'gender': widget
        }
    
    def _clean_fields(self):
        for name, field in self.fields.items():
            # value_from_datadict() gets the data from the data dictionaries.
            # Each widget type knows how to retrieve its own data, because some
            # widgets split data over several HTML fields.
            if field.disabled:
                value = self.get_initial_for_field(field, name)
            else:
                value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
            try:
                if isinstance(field, FileField):
                    initial = self.get_initial_for_field(field, name)
                    value = field.clean(value, initial)
                else:
                    value = field.clean(value)
                self.cleaned_data[name] = value
                if hasattr(self, 'clean_%s' % name):
                    value = getattr(self, 'clean_%s' % name)()
                    self.cleaned_data[name] = value
            except ValidationError as e:
                if name in ('pronoun', 'gender'):
                    self._set_field(name, value)
                    return
                
                self.add_error(name, e)
    
    def _set_field(self, name: str, value: str):
        instance = None
        if name == 'pronoun':
            instance = models.Pronoun.objects.get(name=value)
        elif name == 'gender':
            instance = models.Gender.objects.get(name=value)

        self.cleaned_data[name] = instance
        self.initial[name] = instance.id
        data = self.data.copy()
        data[name] = str(instance.id)
        self.data = data
