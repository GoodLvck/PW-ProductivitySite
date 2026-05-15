from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    color = models.CharField(max_length=7, default="#f59e0b")
