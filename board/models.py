from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date
from trello import settings


class Window(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=30)
    created_date = models.DateTimeField(default=timezone.now)
    update = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(upload_to='images/')
    favourite = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favourite', blank=True)
    archive = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='archive', blank=True)

    def __str__(self):
        return self.title


class WindowArchive(Window):
    pass


class Column(models.Model):
    window = models.ForeignKey('Window', on_delete=models.CASCADE, related_name='columns', null=True)
    title = models.CharField(max_length=30)


    class Meta:
        verbose_name = 'Column'
        verbose_name_plural = 'Columns'

    def __str__(self):
        return self.title


class Entry(models.Model):
    column = models.ForeignKey('Column', on_delete=models.CASCADE, related_name="entries")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=500)
    date_created = models.DateTimeField(default=timezone.now)
    deadline = models.DateTimeField(null=True)
    CHOICES = (
        ('red', 'red'),
        ('blue', 'blue'),
        ('green', 'green'),
        ('yellow', 'yellow')
    )
    choice = models.CharField(max_length=255, choices=CHOICES)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d', blank=True)

    def change_name(self, new_title):
        self.title = new_title
        self.save()
        return self.title == new_title

    def __str__(self):
        return self.title

    @property
    def Days_till(self):
        today = date.today()
        days_till = self.deadline.date() - today
        return days_till

    class Meta:
        verbose_name_plural = "Entries"


class Comment(models.Model):
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
  body = models.CharField(max_length=300)
  created_on = models.DateTimeField(auto_now_add=True, null=True)
  entry = models.ForeignKey('Entry', on_delete=models.CASCADE)