from django import forms
from recruiter.models import JobPost,CompanyDetails


class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = JobPost
        # fields= ['fullname','usertype','job_title','job_description','required_qualifications',
        fields= ['created_by','company','job_title','job_description','required_qualifications',
                 'desired_qualifications','responsibilities','application_deadline','salary_range',
                 'location','employment_type','company_benefits','how_to_apply']





class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyDetails
        fields = ['created_by','company_name','company_details']
