from django.db import models


class ShowTheme(models.Model):
    name = models.CharField(max_length=255)


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    show_theme = models.ManyToManyField(ShowTheme, related_name="astronomy_shows")
