from django.db import models
from django.contrib import admin

# Create your models here.


class Post(models.Model):
    text = models.TextField()
    data = models.DateTimeField()
    temperature = models.FloatField()
    pressure = models.FloatField()
    humidity = models.IntegerField()


class PostAdmin(admin.ModelAdmin):
    list_display = ['text', 'data',
                    'temperature', 'pressure',
                    'humidity',]
