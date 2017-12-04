from django.db import models
from django import forms

# Create your models here.

class Match(models.Model):
    match_id = models.CharField(max_length=50)
    hero1 = models.CharField(max_length=40)
    hero2 = models.CharField(max_length=40)
    hero3 = models.CharField(max_length=40)
    win = models.BooleanField(default=False)

class Data(models.Model):
    title = models.CharField(max_length=20)

class Hero(models.Model):
    hero_id = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    image = models.CharField(max_length=140)

    def __str__(self):
        return self.name

class HeroSelectForm(forms.Form):
    hero1 = forms.ModelChoiceField(Hero.objects, label='',
                                      to_field_name="name")
    hero2 = forms.ModelChoiceField(Hero.objects, label='',
                                      to_field_name="name",
                                      required=False)
    hero3 = forms.ModelChoiceField(Hero.objects, label='',
                                      to_field_name="name",
                                      required=False)

class HeroPickStat(models.Model):
    sample_count = models.IntegerField(default=0)
    hero1 = models.CharField(max_length=40, null=True)
    hero2 = models.CharField(max_length=40, null=True)
    hero3 = models.CharField(max_length=40, null=True)
    win_rate = models.FloatField(default=0.0)
    win_rate_str = models.CharField(max_length=5)
