from django.db import models

class Priority(models.Model):
    priority_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=10)
    def __str__(self):
        return self.name

