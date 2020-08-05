from django.db import models


class Authors(models.Model):
    name = models.CharField(max_length=128)


class Categories(models.Model):
    name = models.CharField(max_length=256)


class Books(models.Model):
    """
    I didn't know which fields should be required, so I assumed only id
    was required.
    """
    id = models.CharField(max_length=32, primary_key=True)
    title = models.CharField(max_length=256, blank=True, null=True)
    authors = models.ManyToManyField(Authors)
    published_date = models.CharField(max_length=4, blank=True, null=True)
    categories = models.ManyToManyField(Categories)
    average_rating = models.FloatField(blank=True, null=True)
    ratings_count = models.IntegerField(blank=True, null=True)
    thumbnail = models.TextField(blank=True, null=True)
