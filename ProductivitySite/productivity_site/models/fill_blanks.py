from django.db import models
from .summary import Summary

class FillBlanks(models.Model):
    fill_blanks_id = models.IntegerField(primary_key=True)
    summary_id = models.ForeignKey(Summary, on_delete=models.CASCADE)
    text = models.TextField()
    valid_answers = models.CharField(max_length=255)
    hint = models.CharField(max_length=255)
    times_answered = models.IntegerField(default=0)
    times_correct = models.IntegerField(default=0)
    def __str__(self):
        return f"Fill blanks #{self.fill_blanks_id}"

