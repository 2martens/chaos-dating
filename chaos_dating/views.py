# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render


def index(request) -> HttpResponse:
    context = {
        'site': {
            'title': 'Chaos Dating'
        }
    }
    if request.user.is_authenticated:
        return render(request, template_name='chaos_dating/home.html', context=context)
    else:
        return render(request, template_name='chaos_dating/landing.html', context=context)


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
