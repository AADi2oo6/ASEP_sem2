from django.db import models
# Create your models here.

class login(models.Model):
    userName= models.EmailField()
    Password = models.CharField(max_length=10)
    BRANCH_CHOICES = [
        ('AIML', 'Artificial Intelligence and Machine Learning'),
        ('CS', 'Computer Science'),
        ('AIDS', 'Artificial Intelligence and Data Science'),
    ]
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES, default=None, null=True, blank=True)
    div = models.CharField(max_length=1, default=None, null=True, blank=True)

class Flogin(models.Model):
    userName = models.EmailField()
    Password = models.CharField(max_length=10)

