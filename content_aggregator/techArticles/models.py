from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200)
    desc = models.TextField()
    pubDate = models.DateTimeField()
    link = models.URLField()
    author = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    guid = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return f"{self.title} : {self.author}"