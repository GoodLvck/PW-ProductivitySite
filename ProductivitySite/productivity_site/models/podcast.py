from django.db import models
from .summary import Summary

class Podcast(models.Model):
    podcast_id = models.IntegerField(primary_key=True)
    summary_id = models.OneToOneField(Summary, on_delete=models.CASCADE)
    text = models.TextField()
