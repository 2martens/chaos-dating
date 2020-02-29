# coding=utf-8
from django.contrib.auth.models import User
from django.core import validators
from django.db import models
from django.utils.translation import gettext as _


class Gender(models.Model):
    name = models.CharField(max_length=16, unique=True)
    
    def __str__(self):
        return self.name


class Interest(models.Model):
    name = models.CharField(max_length=32, unique=True)
    
    def __str__(self):
        return self.name
    

class Pronoun(models.Model):
    name = models.CharField(max_length=32, unique=True)
    
    def __str__(self):
        return self.name


class Wish(models.Model):
    interest = models.ForeignKey(Interest, models.CASCADE)
    gender = models.ForeignKey(Gender, models.CASCADE, null=True, blank=True)
    
    class Meta:
        unique_together = ["interest", "gender"]
    
    def __str__(self):
        if self.gender is not None:
            return f"{self.interest} {_('with')} {self.gender} {_('humans')}"
        else:
            return f"{self.interest}"


class Profile(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    
    age = models.PositiveIntegerField(_('Age'), validators=[validators.MinValueValidator(1),
                                                            validators.MaxValueValidator(100)])
    gender = models.ForeignKey(Gender, models.SET_NULL, null=True)
    pronoun = models.ForeignKey(Pronoun, models.SET_NULL, null=True)
    wishes = models.ManyToManyField(Wish, blank=True)
    
    def __str__(self):
        return self.user.username
