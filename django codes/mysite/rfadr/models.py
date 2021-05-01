import datetime

from django.db import models
from django.utils import timezone

class Rfadd(models.Model):
    rf_adr = models.CharField(max_length = 100)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.rf_adr

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Modstatus(models.Model):
    status = models.CharField(max_length = 100)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.status

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)