# coding=utf-8
from django.urls import path

from . import views

app_name = 'chaos_dating'
urlpatterns = [
    path('', views.index, name='index'),
    path('legal-notice/', views.legal, name='legal'),
    path('privacy/', views.privacy, name='privacy'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]
