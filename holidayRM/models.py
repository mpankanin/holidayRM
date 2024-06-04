from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Vacation(models.Model):
    """
    This model represents a vacation period for a user.

    Attributes:
        date_from (DateField): The start date of the vacation.
        date_to (DateField): The end date of the vacation.
        user (ForeignKey): The user who is taking the vacation.
        is_approved (BooleanField): Whether the vacation has been approved.
    """
    date_from = models.DateField(default=timezone.now())
    date_to = models.DateField(default=timezone.now())
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
