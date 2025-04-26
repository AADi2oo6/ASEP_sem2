from django.db import models

# Create your models here.
class login(models.Model):
    SEM_CHOICES = [(str(i), str(i)) for i in range(1, 8 + 1)]  # 1 to 8
    BATCH_CHOICE =[("1","1"),('2','2'),("3","3")]

    Name = models.CharField(max_length=40,default=None,null = True)
    semester = models.CharField(max_length=2, choices=SEM_CHOICES,default=None,null = True)
    userName= models.EmailField()
    Password = models.CharField(max_length=10)
    branch = models.CharField(max_length=10, default=None, null=True, blank=True)
    div = models.CharField(max_length=1, default=None, null=True, blank=True)
    batch = models.CharField(max_length=1,choices=BATCH_CHOICE, default=None,null = True)

class Flogin(models.Model):
    userName = models.EmailField()
    Password = models.CharField(max_length=10)

