from django.shortcuts import render, redirect
from .forms import JobApplicationForm
from django.contrib.auth import authenticate, login,logout
from account.models import User
from recruiter.models import JobPost,CompanyDetails
from job_seeker.models import JobApplication
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View
from django.db.models import Q
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404


# Create your views here.
@login_required
def job_seeker_dashboard(request):
    try:
        return render(request, 'job_seeker_dashboard.html')

    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@login_required
def job_listings(request):
    try:
        jobs = JobPost.objects.exclude(job_title__isnull=True, id__isnull=True)

        keyword = request.GET.get('keyword', '')
        location = request.GET.get('location', '')

        # Filter jobs based on search parameters
        if keyword:
            jobs = jobs.filter(
                Q(created_by__username__icontains=keyword) |  # Use created_by to get the recruiter's username
                Q(job_title__icontains=keyword) |
                Q(job_description__icontains=keyword) |
                Q(required_qualifications__icontains=keyword) |
                Q(desired_qualifications__icontains=keyword) |
                Q(responsibilities__icontains=keyword)
            )

        if location:
            jobs = jobs.filter(location__icontains=location)

        jobs = jobs.exclude(job_title=None, job_description=None, required_qualifications=None, location=None)

        # Sorting - Default to sorting by application_deadline
        sort_by = request.GET.get('sort_by', 'application_deadline')  # Use '-' to indicate descending order
        if sort_by not in ['application_deadline']:
            sort_by = 'application_deadline'

        jobs = jobs.order_by(sort_by)

        job_details = []
        for job in jobs:
            job_details.append({
                'recruiter_name': job.created_by.username,
                'company': job.company,
                'created_date': job.created_date,
                'job_title': job.job_title,
                'job_description': job.job_description,
                'required_qualifications': job.required_qualifications,
                'desired_qualifications' : job.desired_qualifications,
                'responsibilities' : job.responsibilities,
                'application_deadline' : job.application_deadline,
                'salary_range' : job.salary_range,
                'location': job.location,
                'company_benefits':job.company_benefits,
                'how_to_apply':job.how_to_apply,
                'employment_type': job.employment_type,
            })

        return render(request, 'job_listings.html', {'job_details': job_details})

    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@login_required
def apply_for_job(request, recruiter_name):
    try:
        # Use get_list_or_404 to handle the case where multiple JobPosts are returned
        jobs = get_list_or_404(JobPost, created_by__username=recruiter_name)

        # Assuming you want to work with the first job in the list
        job = jobs[0]

        existing_application = JobApplication.objects.filter(job=job, applicant=request.user).first()

        if existing_application:
            return render(request, 'already_applied.html', {'job': job, 'existing_application': existing_application})

        if request.method == 'POST':
            form = JobApplicationForm(request.POST, request.FILES)
            if form.is_valid():
                application = form.save(commit=False)
                application.applicant = request.user
                application.save()
                application.job.add(job)  # Use the add() method for many-to-many relationships
                return redirect('applied_jobs')  # Redirect to job listings or a thank you page
        else:
            form = JobApplicationForm()

        return render(request, 'apply_for_job.html', {'form': form, 'job': job})

    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@login_required
def applied_jobs(request):
    try:
        # Assuming the logged-in user is a job seeker
        job_seeker = request.user

        # Retrieve applications submitted by the job seeker
        applications = JobApplication.objects.filter(applicant=job_seeker)

        applied_jobs_list = []
        for application in applications:
            # Iterate through all jobs associated with the application
            for job in application.job.all():
                applied_job_details = {
                    'company_name': job.company.company_name if job.company else '',  # Assuming CompanyDetails has a 'company_name' field
                    'job_title': job.job_title,
                    'application_status': application.status,
                }
                applied_jobs_list.append(applied_job_details)

        return render(request, 'applied_jobs.html', {'applied_jobs_list': applied_jobs_list})

    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@login_required
def company_details_page(request):
    try:
        # Fetch all company details
        company_details = CompanyDetails.objects.all()

        return render(request, 'company_details_page.html', {'company_details': company_details})

    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})


