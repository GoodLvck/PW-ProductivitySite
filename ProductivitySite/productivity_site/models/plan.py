from django.db import models

class Plan(models.Model):
    plan_id = models.IntegerField(primary_key=True)
    plan_name = models.CharField(max_length=100, unique=True)
    plan_description = models.TextField()
    price = models.FloatField()