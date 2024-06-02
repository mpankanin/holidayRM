from django.db import models
from django.utils import timezone


class Vacation(models.Model):
    dateFrom = models.DateField(default=timezone.now())
    dateTo = models.DateField(default=timezone.now())

