from django.db import models

from productivity_site.models.task import Task

class Subtask(models.Model):
    PRIORITY_LOW = "low"
    PRIORITY_MEDIUM = "medium"
    PRIORITY_HIGH = "high"

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, "Low"),
        (PRIORITY_MEDIUM, "Medium"),
        (PRIORITY_HIGH, "High"),
    ]

    subtask_id = models.IntegerField(primary_key=True)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField()
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default=PRIORITY_MEDIUM,
    )
    estimated_time = models.IntegerField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

