from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

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
    estimated_time = models.PositiveIntegerField()
    completed = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["task_id", "name"],
                name="unique_subtask_name_per_task",
            )
        ]

    def clean(self):
        if self.due_date and self.due_date < timezone.now():
            raise ValidationError({"due_date": "Due date cannot be in the past"})
        if self.task_id_id and self.due_date and self.due_date > self.task_id.due_date:
            raise ValidationError({"due_date": "Subtask due date cannot be after the task due date"})
        if self.estimated_time is not None and self.estimated_time <= 0:
            raise ValidationError({"estimated_time": "Estimated time must be greater than 0"})

    def __str__(self):
        return self.name
