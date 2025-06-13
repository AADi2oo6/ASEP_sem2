from django.db import models

class Announcement(models.Model):
    subject = models.CharField(max_length=100)
    content = models.TextField()
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    
    # Target audience fields
    years = models.JSONField(default=list)    # e.g. ["FY", "SY"]
    branches = models.JSONField(default=list) # e.g. ["CS", "AIDS"]
    sections = models.JSONField(default=list) # e.g. ["A", "B"]
    batches = models.JSONField(default=list)  # e.g. ["1", "2"]

    # Teacher details
    teacher_id = models.CharField(max_length=20)
    teacher_name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    # List of identifier names
   

    def __str__(self):
        return f"{self.subject} ({self.teacher_name})"
