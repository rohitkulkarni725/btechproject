import datetime

from django.db import models
from django.utils import timezone

class Modules(models.Model):
    num_mod = models.CharField(max_length = 100)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.num_mod

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)