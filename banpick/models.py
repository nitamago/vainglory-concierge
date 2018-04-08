from django.db import models
from django import forms

# Create your models here.
class Pick_Seq(models.Model):
    match_id = models.CharField(max_length=50)
    pick1 = models.CharField(max_length=40)
    pick2 = models.CharField(max_length=40)
    pick3 = models.CharField(max_length=40)
    pick4 = models.CharField(max_length=40)
    pick5 = models.CharField(max_length=40)
    pick6 = models.CharField(max_length=40)
    pick7 = models.CharField(max_length=40)
    pick8 = models.CharField(max_length=40)
    pick9 = models.CharField(max_length=40)
    pick10 = models.CharField(max_length=40)
    pick11 = models.CharField(max_length=40)
    pick12 = models.CharField(max_length=40)
    pick13 = models.CharField(max_length=40)
    pick14 = models.CharField(max_length=40)
    left_win = models.BooleanField(default=False)
    right_win = models.BooleanField(default=False)

class Hero(models.Model):
    hero_id = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    image = models.CharField(max_length=140)
    feature = models.CharField(max_length=400)

    def __str__(self):
        return self.name

class Seq_Cache(models.Model):
    target = models.CharField(max_length=40)
    key_str = models.CharField(max_length=400)
    index = models.IntegerField()
    pick_rate = models.CharField(max_length=40)
    win_rate = models.CharField(max_length=40)
    lose_rate = models.CharField(max_length=40)

class Pick_Info(forms.Form):
    pick_str = forms.CharField()
    pick_str.widget = forms.HiddenInput()

