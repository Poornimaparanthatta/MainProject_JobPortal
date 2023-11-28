from django.db import models
from account.models import User
from recruiter.models import JobPost

# Create your models here.
class JobApplication(models.Model):
    job = models.ManyToManyField(JobPost)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(null=True)
    resume_for_applying = models.FileField(upload_to='applications/', null=True)
    application_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )

