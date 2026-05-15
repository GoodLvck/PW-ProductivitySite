from django.db import models
from .summary import Summary

class Flashcard(models.Model):
    flashcard_id = models.IntegerField(primary_key=True)
    summary_id = models.ForeignKey(Summary, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    valid_answers = models.CharField(max_length=255)
    hint = models.CharField(max_length=255)
    times_answered = models.IntegerField(default=0)
    times_correct = models.IntegerField(default=0)
    def __str__(self):
        return self.question

