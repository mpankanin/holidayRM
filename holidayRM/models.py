from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Vacation(models.Model):
    dateFrom = models.DateField(default=timezone.now())
    dateTo = models.DateField(default=timezone.now())
    user = models.ForeignKey(User, on_delete=models.CASCADE)
