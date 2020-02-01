# coding=utf-8
from django.contrib.auth import views as auth_views
from django.urls import path

from chaos_dating import views as chaos_views

extra_context = {
    'site': {
        'title': 'Chaos Dating'
    },
}

urlpatterns = [
    path('login/', chaos_views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('register/', chaos_views.register, name='register'),

    path('password_change/',
         auth_views.PasswordChangeView.as_view(extra_context=extra_context),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(extra_context=extra_context),
         name='password_change_done'),

    path('password_reset/',
         auth_views.PasswordResetView.as_view(extra_context=extra_context),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(extra_context=extra_context),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(extra_context=extra_context),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(extra_context=extra_context),
         name='password_reset_complete'),
    path('edit_profile/', chaos_views.edit_profile, name='edit_profile'),
]
