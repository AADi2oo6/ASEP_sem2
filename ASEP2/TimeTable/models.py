from django.db import models
from .branches import BRANCHES_CHOICES
class StudentsTT(models.Model):
    DAYS_CHOICES = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
    ]

    TIME_SLOT_CHOICES = [
        ("8-9 AM", "8-9 AM"),
        ("9-10 AM", "9-10 AM"),
        ("10-11 AM", "10-11 AM"),
        ("11-12 PM", "11-12 PM"),
        ("12-1 PM", "12-1 PM"),
        ("1-2 PM", "1-2 PM"),
        ("2-3 PM", "2-3 PM"),
        ("3-4 PM", "3-4 PM"),
        ("4-5 PM", "4-5 PM"),
        ("5-6 PM", "5-6 PM"),
    ]

    CLASS_TYPE_CHOICES = [
        ("Theory", "Theory"),
        ("Lab", "Lab"),
        ("Tutorial", "Tutorial"),
    ]

    SEM_CHOICES = [(str(i), str(i)) for i in range(1, 8 + 1)]  # 1 to 8

    BATCH_CHOICES = [
        ("all", "All"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
    ]
    YEAR_CHOICES = {
        ("FY","FY"),
        ("SY","SY"),
        ("TY","TY"),
        ("4Y","4Y")
    }

    day = models.CharField(max_length=10, choices=DAYS_CHOICES)
    course_name = models.CharField(max_length=100,default="AIML",choices=BRANCHES_CHOICES)
    div = models.CharField(max_length=1,default="A")
    semester = models.CharField(max_length=2, choices=SEM_CHOICES)
    year = models.CharField(max_length=2, default=None, null=True, choices=YEAR_CHOICES)
    time_slot = models.CharField(max_length=10, choices=TIME_SLOT_CHOICES)
    room_no = models.CharField(max_length=10)
    subject_name = models.CharField(max_length=100)
    teacher_name = models.CharField(max_length=100)
    class_type = models.CharField(max_length=10, choices=CLASS_TYPE_CHOICES)
    batch = models.CharField(max_length=10, choices=BATCH_CHOICES, default="all")

    def __str__(self):
        return f"{self.course_name} - {self.subject_name} ({self.day} {self.time_slot})"

from login.models import Flogin

class FacultysTT(models.Model):
    DAYS_CHOICES = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
    ]

    TIME_SLOT_CHOICES = [
        ("8-9 AM", "8-9 AM"),
        ("9-10 AM", "9-10 AM"),
        ("10-11 AM", "10-11 AM"),
        ("11-12 PM", "11-12 PM"),
        ("12-1 PM", "12-1 PM"),
        ("1-2 PM", "1-2 PM"),
        ("2-3 PM", "2-3 PM"),
        ("3-4 PM", "3-4 PM"),
        ("4-5 PM", "4-5 PM"),
        ("5-6 PM", "5-6 PM"),
    ]

    CLASS_TYPE_CHOICES = [
        ("Theory", "Theory"),
        ("Lab", "Lab"),
        ("Tutorial", "Tutorial"),
    ]

    SEM_CHOICES = [(str(i), str(i)) for i in range(1, 8 + 1)]  # 1 to 8

    BATCH_CHOICES = [
        ("all", "All"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
    ]
    YEAR_CHOICES = {
        ("FY","FY"),
        ("SY","SY"),
        ("TY","TY"),
        ("4Y","4Y")
    }

    teachersID = models.IntegerField(default=00000)
    teacher_name = models.ForeignKey(Flogin, on_delete=models.SET_NULL, null=True, related_name="timetable_entries")
    day = models.CharField(max_length=10, choices=DAYS_CHOICES)
    time_slot = models.CharField(max_length=10, choices=TIME_SLOT_CHOICES)
    room_no = models.CharField(max_length=10)
    year = models.CharField(max_length=2, default=None, null=True, choices=YEAR_CHOICES)
    semester = models.CharField(max_length=2,default="NA", choices=SEM_CHOICES)
    course_name = models.CharField(max_length=100, choices=BRANCHES_CHOICES)
    div = models.CharField(max_length=1,default="A")
    subject_name = models.CharField(max_length=100)
    # branchName = models.CharField(max_length=100)
    class_type = models.CharField(max_length=10, choices=CLASS_TYPE_CHOICES)
    batch = models.CharField(max_length=10, choices=BATCH_CHOICES, default="all")

    def __str__(self):
        return f"{self.course_name} - {self.subject_name} ({self.day} {self.time_slot})"

