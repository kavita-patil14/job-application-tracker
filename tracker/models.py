from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import date, timedelta

class JobApplication(models.Model):
    JOB_STATUS_CHOICES = [
        ("Applied", "Applied"),
        ("Not Applied", "Not Applied"),
        ("Interview Scheduled", "Interview Scheduled"),
        ("Exam Scheduled", "Exam Scheduled"),
        ("Offer Received", "Offer Received"),
        ("Rejected", "Rejected"),
        ("Accepted", "Accepted"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    applied_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=JOB_STATUS_CHOICES, default="Applied")

    deadline = models.DateField(null=True, blank=True)

    job_link = models.URLField(max_length=500, blank=True, null=True)

    def is_urgent(self):
        if self.deadline:
            return self.deadline <= date.today() + timedelta(days=3)
        return False


    def __str__(self):
        return f"{self.job_title} at {self.company_name} ({self.status})"

