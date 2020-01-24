# coding=utf-8
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from chaos_dating.models import Profile, Pronoun
from chaos_dating.models import Gender
from chaos_dating.models import Interest
from chaos_dating.models import Wish

# Register your models here.
admin.site.unregister(User)


class ProfileInline(admin.StackedInline):
    model = Profile
    filter_horizontal = ('wishes',)


class UserProfileAdmin(UserAdmin):
    inlines = [ProfileInline, ]


admin.site.register(User, UserProfileAdmin)

admin.site.register(Pronoun)
admin.site.register(Profile)
admin.site.register(Gender)
admin.site.register(Interest)
admin.site.register(Wish)
