from django.db import models
from productivity_site.models import Summary

class Podcast(models.Model):
    podcas_id = models.IntegerField(primary_key=True)
    summary_id = models.OneToOneField(Summary, on_delete=models.CASCADE)
    text = models.TextField()