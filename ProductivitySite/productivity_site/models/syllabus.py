from django.db import models
from .subject import Subject

class Syllabus(models.Model):
    syllabus_id = models.IntegerField(primary_key=True)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
