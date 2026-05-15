from django.db import models
from django.contrib.auth.models import User


class FreeTime(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    monday = models.IntegerField(default=0)
    tuesday = models.IntegerField(default=0)
    wednesday = models.IntegerField(default=0)
    thursday = models.IntegerField(default=0)
    friday = models.IntegerField(default=0)
    saturday = models.IntegerField(default=0)
    sunday = models.IntegerField(default=0)

    def __str__(self):
        return f"Free time - {self.user_id}"
