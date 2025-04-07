from django.db import models
# Create your models here.

class login(models.Model):
    role =models.CharField(max_length=30)
    userName= models.EmailField()
    Password = models.CharField(max_length=10)

