# coding=utf-8
from django.urls import path

from . import views

app_name = 'chaos_dating'
urlpatterns = [
    path('', views.index, name='index'),
    path('users/<str:username>', views.profile, name='profile'),
    path('filter/', views.filter, name='filter'),
    path('rest/filter/', views.filter_rest, name='filterREST'),
    path('legal-notice/', views.legal, name='legal'),
    path('privacy/', views.privacy, name='privacy'),
]
