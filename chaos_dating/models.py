# coding=utf-8
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Gender(models.Model):
    name = models.CharField(max_length=16, unique=True)
    
    def __str__(self):
        return self.name


class Interest(models.Model):
    name = models.CharField(max_length=32, unique=True)
    
    def __str__(self):
        return self.name


class Wish(models.Model):
    interest = models.ForeignKey(Interest, models.CASCADE)
    gender = models.ForeignKey(Gender, models.CASCADE, null=True, blank=True)
    
    class Meta:
        unique_together = ["interest", "gender"]
    
    def __str__(self):
        return '%s with %ss' % (self.interest, self.gender)


class Profile(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    
    gender = models.ForeignKey(Gender, models.SET_NULL, null=True)
    wishes = models.ManyToManyField(Wish)
    
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
