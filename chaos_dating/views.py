# coding=utf-8
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext as _

from chaos_dating import models
from chaos_dating.forms import FilterForm
from chaos_dating.forms import ProfileForm
from chaos_dating.forms import UserForm


def index(request) -> HttpResponse:
    context = {
        'site': {
            'title': 'Chaos Dating'
        }
    }
    if request.user.is_authenticated:
        profiles = models.Profile.objects.all()
        context['profiles'] = profiles
        context['filter_form'] = FilterForm()
        return render(request, template_name='chaos_dating/home.html', context=context)
    else:
        return render(request, template_name='chaos_dating/landing.html', context=context)


@login_required()
def filter(request) -> HttpResponse:
    context = {
        'site': {
            'title': 'Chaos Dating'
        }
    }
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            profiles = models.Profile.objects.all()
            if cleaned_data['gender']:
                profiles = profiles.filter(gender__in=cleaned_data['gender'])
            if cleaned_data['wishes']:
                profiles = profiles.filter(wishes__in=cleaned_data['wishes'])
            if cleaned_data['order_by'] and cleaned_data['order_direction']:
                sort_order = '-' if cleaned_data['order_direction'] == '-' else ''
                profiles = profiles.order_by(f"{sort_order}{cleaned_data['order_by']}")
            if cleaned_data['min_age']:
                profiles = profiles.filter(age__gte=cleaned_data['min_age'])
            if cleaned_data['max_age']:
                profiles = profiles.filter(age__lte=cleaned_data['max_age'])
            context['profiles'] = profiles
        
        context['filter_form'] = form
    
    else:
        profiles = models.Profile.objects.all()
        context['profiles'] = profiles
        context['filter_form'] = FilterForm()
        
    return render(request, template_name='chaos_dating/home.html', context=context)


@login_required()
def filter_rest(request) -> JsonResponse:
    if request.method != 'POST':
        return JsonResponse({})
    
    form = FilterForm(request.POST)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        profiles = models.Profile.objects.all()
        if cleaned_data['gender']:
            profiles = profiles.filter(gender__in=cleaned_data['gender'])
        if cleaned_data['wishes']:
            profiles = profiles.filter(wishes__in=cleaned_data['wishes'])
        if cleaned_data['order_by'] and cleaned_data['order_direction']:
            sort_order = '-' if cleaned_data['order_direction'] == '-' else ''
            profiles = profiles.order_by(f"{sort_order}{cleaned_data['order_by']}")
        if cleaned_data['min_age']:
            profiles = profiles.filter(age__gte=cleaned_data['min_age'])
        if cleaned_data['max_age']:
            profiles = profiles.filter(age__lte=cleaned_data['max_age'])
        
        context = {
            'profiles': profiles
        }
        
        return JsonResponse({
            'profiles': render_to_string('chaos_dating/profiles.html', context=context, request=request),
        })


@transaction.atomic
def register(request) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('chaos_dating:index')
    
    user_form = UserCreationForm(data=request.POST or None)
    profile_form = ProfileForm(data=request.POST or None, files=request.FILES or None)
    context = {
        'site':         {
            'title': 'Chaos Dating'
        },
        'user_form':    user_form,
        'profile_form': profile_form
    }
    if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():
        user = user_form.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        if 'profile_pic' in request.FILES:
            profile.profile_pic = request.FILES['profile_pic']
        profile.save()
        login(request, user=user)
        messages.success(request, _('User was successfully registered'))
        return redirect('edit_profile')
    
    return render(request, template_name='registration/register.html', context=context)


def user_login(request) -> HttpResponse:
    login_view = LoginView()
    login_view.setup(request)
    login_view.redirect_authenticated_user = True
    login_view.extra_context = {
        'active': 'login',
        'title':  _('Login'),
        'site':   {
            'title': 'Chaos Dating'
        },
    }
    return login_view.dispatch(request)


@login_required()
def profile(request, username: str) -> HttpResponse:
    context = {
        'site': {
            'title': 'Chaos Dating'
        },
        'profile': models.Profile.objects.get(user__username=username)
    }
    
    return render(request, template_name='chaos_dating/profile.html', context=context)


@login_required()
@transaction.atomic
def edit_profile(request) -> HttpResponse:
    user_form = UserForm(data=request.POST or None, instance=request.user)
    profile_form = ProfileForm(data=request.POST or None, files=request.FILES or None,
                               instance=request.user.profile)
    user_form.fields['email'].help_text = _('The email address is required for password recovery.')
    context = {
        'active':       'edit_profile',
        'title':        _('Edit User Profile'),
        'site':         {
            'title': 'Chaos Dating'
        },
        'user_form':    user_form,
        'profile_form': profile_form
    }
    
    if request.method == "POST":
        post = request.POST.copy()
        pronoun_input = post['pronoun']
        gender_input = post['gender']
        try:
            int(pronoun_input)
        except ValueError:
            pronoun = models.Pronoun(name=pronoun_input)
            pronoun.save()
            post['pronoun'] = str(pronoun.id)
            request.POST = post
        try:
            int(gender_input)
        except ValueError:
            gender = models.Gender(name=gender_input)
            gender.save()
            post['gender'] = str(gender.id)
            request.POST = post
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            messages.success(request, _('Profile was successfully updated'))
    
    return render(request, template_name='registration/edit_profile.html', context=context)


@login_required()
def password_change_done(request) -> HttpResponse:
    messages.success(request, _('Your password was successfully changed.'))
    return redirect(reverse('edit_profile'))


def legal(request) -> HttpResponse:
    context = {
        'site': {
            'title': 'Chaos Dating'
        }
    }
    return render(request, template_name='chaos_dating/legal.html', context=context)


def privacy(request) -> HttpResponse:
    context = {
        'site': {
            'title': 'Chaos Dating'
        }
    }
    return render(request, template_name='chaos_dating/privacy.html', context=context)
