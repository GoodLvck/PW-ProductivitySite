from django.db import models
from productivity_site.models import Summary

class Multioption(models.Model):
    multioption_id = models.IntegerField(primary_key=True)
    summary_id = models.ForeignKey(Summary, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    valid_answers = models.CharField(max_length=255)
    hint = models.CharField(max_length=255)
    answer1 = models.CharField(max_length=255)
    answer2 = models.CharField(max_length=255)
    answer3 = models.CharField(max_length=255)
    answer4 = models.CharField(max_length=255)
    times_answered = models.IntegerField(default=0)
    times_correct = models.IntegerField(default=0)
