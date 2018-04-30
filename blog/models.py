from django.db import models
from django.utils import timezone

# Create your models here.
class Article(models.Model):
    art_id = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    abstract = models.CharField(max_length=500)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    tags = models.CharField(max_length=100)
    is_public = models.BooleanField(default=False)



