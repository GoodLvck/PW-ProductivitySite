from django.db import models

from productivity_site.models.subject import Subject
from productivity_site.models.priority import Priority


class Task(models.Model):
    task_id = models.IntegerField(primary_key=True)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    text = models.TextField()
    due_date = models.DateTimeField()
    priority_id = models.ForeignKey(Priority, on_delete=models.RESTRICT)
    estimated_time = models.IntegerField()
