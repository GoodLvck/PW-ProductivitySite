from django.db import models
from productivity_site.models import User


class Free_Time(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    monday = models.IntegerField(default=0)
    tuesday = models.IntegerField(default=0)
    wednesday = models.IntegerField(default=0)
    thursday = models.IntegerField(default=0)
    friday = models.IntegerField(default=0)
    saturday = models.IntegerField(default=0)
    sunday = models.IntegerField(default=0)