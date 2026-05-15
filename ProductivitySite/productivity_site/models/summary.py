from django.db import models
from .syllabus import Syllabus

class Summary(models.Model):
    summary_id = models.IntegerField(primary_key=True)
    syllabus_id = models.OneToOneField(Syllabus, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    formatted_text = models.TextField()
