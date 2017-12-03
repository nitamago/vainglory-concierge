from django.db import models

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
