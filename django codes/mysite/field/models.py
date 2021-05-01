import datetime

from django.db import models
from django.utils import timezone

class Moisture(models.Model):
    mois_field = models.CharField(max_length = 100)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.mois_field

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Temperature(models.Model):
    temp_field = models.CharField(max_length = 100)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.temp_field

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Humidity(models.Model):
    hum_field = models.CharField(max_length = 100)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.hum_field

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Light(models.Model):
    int_field = models.CharField(max_length = 100)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.int_field

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)