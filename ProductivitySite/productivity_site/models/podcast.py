from django.db import models
from .summary import Summary

class Podcast(models.Model):
    podcast_id = models.IntegerField(primary_key=True)
    summary_id = models.OneToOneField(Summary, on_delete=models.CASCADE)
    text = models.TextField()
    def __str__(self):
        return f"Podcast #{self.podcast_id}"

