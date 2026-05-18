from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    color = models.CharField(
        max_length=7,
        default="#f59e0b",
        validators=[
            RegexValidator(
                regex=r"^#[0-9a-fA-F]{6}$",
                message="Color must be a valid hex color.",
            )
        ],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_id", "name"],
                name="unique_subject_name_per_user",
            )
        ]

    def __str__(self):
        return self.name
