from django.db import models

from productivity_site.models.priority import Priority
from productivity_site.models.task import Task

class Subtask(models.Model):
    subtask_id = models.IntegerField(primary_key=True)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField()
    priority_id = models.ForeignKey(Priority, on_delete=models.RESTRICT)
    estimated_time = models.IntegerField()
    def __str__(self):
        return self.name

