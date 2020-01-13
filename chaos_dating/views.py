# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render


def index(request) -> HttpResponse:
    context = {
        'site': {
            'title': 'Chaos Dating'
        }
    }
    return render(request, template_name='chaos_dating/index.html', context=context)
