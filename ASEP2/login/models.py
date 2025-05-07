from django.db import models

# Create your models here.
class login(models.Model):
    SEM_CHOICES = [(str(i), str(i)) for i in range(1, 8 + 1)]  # 1 to 8
    BATCH_CHOICE =[("1","1"),('2','2'),("3","3")]
    YEAR_CHOICES = {
        ("FY","FY"),
        ("SY","SY"),
        ("TY","TY"),
        ("4Y","4Y")
    }

    Name = models.CharField(max_length=40,default=None,null = True)
    semester = models.CharField(max_length=2, choices=SEM_CHOICES,default=None,null = True)
    year = models.CharField(max_length=2, default=None, null=True, choices=YEAR_CHOICES)
    userName= models.EmailField()
    Password = models.CharField(max_length=10)
    course_name = models.CharField(max_length=10, default=None, null=True, blank=True)
    div = models.CharField(max_length=1, default=None, null=True, blank=True)
    batch = models.CharField(max_length=1,choices=BATCH_CHOICE, default=None,null = True)

class Flogin(models.Model):
    RANK_CHOICES = {
        ("Professor","Professor"),
        ("Assistant Professor","Assistant Professor")
    }
    teachersID = models.IntegerField(default=00000)
    dept = models.CharField(max_length=50,default=None,null = True)
    Name = models.CharField(max_length=50,default=None,null = True)
    rank = models.CharField(max_length=50, default=None, null=True, choices=RANK_CHOICES)
    userName = models.EmailField(default="xyz@vit.edu")
    Password = models.CharField(max_length=10, default="vitpune")

    def __str__(self):
        return self.Name

