from django.contrib import admin
from account.models import User
from job_seeker.models import JobApplication
from recruiter.models import CompanyDetails,JobPost
# Register your models here.

admin.site.register(User)
admin.site.register(JobApplication)
admin.site.register(JobPost)
admin.site.register(CompanyDetails)