# coding=utf-8

from django.urls import path

from . import views

app_name = 'chaos_dating'
urlpatterns = [
    path('', views.index, name='index')
]
