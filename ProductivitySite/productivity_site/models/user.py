from django.db import models

class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True) # clase de django que comprueba que se parezca a un email real
    phone = models.IntegerField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)