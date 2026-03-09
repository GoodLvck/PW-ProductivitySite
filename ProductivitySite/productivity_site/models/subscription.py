from django.db import models
from productivity_site.models import User, Plan

class Subscription(models.Model):
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    billing_date = models.DateTimeField()
    end_date = models.DateTimeField()
    autobilling = models.BooleanField(default=False)