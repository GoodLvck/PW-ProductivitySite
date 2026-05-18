from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from productivity_site.models.subject import Subject

class Task(models.Model):
    PRIORITY_LOW = "low"
    PRIORITY_MEDIUM = "medium"
    PRIORITY_HIGH = "high"

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, "Low"),
        (PRIORITY_MEDIUM, "Medium"),
        (PRIORITY_HIGH, "High"),
    ]

    task_id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    text = models.TextField()
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
                fields=["subject_id", "name"],
                name="unique_task_name_per_subject",
            )
        ]

    def clean(self):
        if self.due_date and self.due_date < timezone.now():
            raise ValidationError({"due_date": "Due date cannot be in the past"})
        if self.estimated_time is not None and self.estimated_time <= 0:
            raise ValidationError({"estimated_time": "Estimated time must be greater than 0"})

    def __str__(self):
        return self.name
