from django.db import models
from account.models import User

# Create your models here.
class CompanyDetails(models.Model):
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    company_name = models.CharField(max_length=50)
    company_details = models.TextField(null=True)


    def __str__(self):
        return self.company_name


class JobPost(models.Model):
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    created_date = models.DateField(auto_now=True)
    company = models.ForeignKey(CompanyDetails,on_delete=models.CASCADE,null=True)
    job_title = models.CharField(max_length=100,null=True)
    job_description = models.TextField(null=True,blank=True)
    required_qualifications = models.TextField(null=True,blank=True)
    desired_qualifications = models.TextField(null=True,blank=True)
    responsibilities = models.TextField(null=True,blank=True)
    application_deadline = models.DateField(null=True,blank=True)
    salary_range = models.CharField(max_length=50,null=True,blank=True)
    location = models.CharField(max_length=50,null=True,blank=True)
    employment_type_choice = [
        ('Full-time','Full-time'),
        ('Part-time','Part-time'),
        ('Contract','Contract')
    ]
    employment_type = models.CharField(max_length=50,choices=employment_type_choice,null=True,blank=True)
    company_benefits = models.TextField(null=True,blank=True)
    how_to_apply = models.TextField(null=True,blank=True)



