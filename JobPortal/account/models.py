from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    Usertype_choice = [
        ('Job Seeker','Job Seeker'),
        ('Recruiter','Recruiter')
    ]
    usertype = models.CharField(max_length=20,choices=Usertype_choice,null=True)
    fullname = models.CharField(max_length=50,null=True)
    bio = models.TextField(null=True,blank=True)
    resume = models.FileField(upload_to='uploads/',null=True)

    @property
    def is_job_seeker(self):
        return self.usertype == 'Job Seeker'

    @property
    def is_recruiter(self):
        return self.usertype == 'Recruiter'


