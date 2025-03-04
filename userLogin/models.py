from django.db import models

# Create your models here.

class User(models.Model):
    userName = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(max_length=20, primary_key=True)