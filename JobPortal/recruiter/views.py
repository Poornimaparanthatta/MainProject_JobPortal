from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import RecruiterProfileForm,CompanyProfileForm
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

# Create your views here.
@login_required
def recruiter_dashboard(request):
    try:
        return render(request, 'recruiter_dashboard.html')

    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@login_required
def recruiter_profile(request):
    try:
        user = request.user

        # Redirect if the user is not authenticated or not a recruiter
        if not user.is_authenticated or not user.is_recruiter:
            return redirect('recruiter_dashboard')

        if request.method == 'POST':
            # Use RecruiterProfileForm to handle JobPost model
            form = RecruiterProfileForm(request.POST,request.FILES)
            if form.is_valid():
                # Create a new JobPost instance and associate it with the current user
                job_post = form.save(commit=False)
                job_post.created_by = user
                job_post.save()

                return redirect('recruiter_dashboard')
        else:
            # Use RecruiterProfileForm to handle JobPost model
            form = RecruiterProfileForm()

        return render(request, 'recruiter_profile.html', {'user': user, 'form': form})

    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@login_required
def edit_job(request, job_post_id):
    try:
        job_post = get_object_or_404(JobPost, pk=job_post_id, created_by=request.user)

        if request.method == 'POST':
            form = RecruiterProfileForm(request.POST, instance=job_post)
            if form.is_valid():
                form.save()
                return redirect('recruiter_dashboard')
        else:
            form = RecruiterProfileForm(instance=job_post)

        return render(request, 'edit_job.html', {'form': form, 'job_post': job_post})

    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@login_required
def delete_job(request, job_post_id):
    try:
        job_post = get_object_or_404(JobPost, pk=job_post_id, created_by=request.user)

        if request.method == 'POST':
            job_post.delete()
            return redirect('recruiter_dashboard')

        return render(request, 'delete_job.html', {'job_post': job_post})

    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@login_required
def recruiter_dashboardd(request):
    try:
        user = request.user

        if not user.is_authenticated or not user.is_recruiter:
            return redirect('index')

        job_posts = JobPost.objects.filter(created_by=user)
        return render(request, 'recruiter_data.html', {'job_posts': job_posts})

    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@login_required
def recruiter_applications(request):
    try:
        # Assuming the logged-in user is a recruiter
        recruiter = request.user

        # Retrieve jobs posted by the recruiter
        jobs = JobPost.objects.filter(created_by=recruiter)

        # Retrieve applications associated with the recruiter's jobs
        applications = JobApplication.objects.filter(job__in=jobs)

        application_details_list = []
        for application in applications:
            # Iterate through all jobs associated with the application
            for job in application.job.all():
                application_details = {
                    'cover_letter': application.cover_letter,
                    'resume_for_applying': application.resume_for_applying,
                    'application_date': application.application_date,
                    'job_title': job.job_title,  # Access the job title from the related job
                    'applicant_name': application.applicant.fullname,
                    'status': application.status,
                }
                application_details_list.append(application_details)

        # Pass the list of application details and job titles to the template
        job_titles = [app['job_title'] for app in application_details_list]

        return render(request, 'recruiter_applications.html',
                      {'applications': application_details_list, 'job_titles': job_titles})

    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@login_required
def update_application_status(request, applicant_name):
    try:
        applications = JobApplication.objects.filter(applicant__fullname=applicant_name)

        if request.method == 'POST':
            new_status = request.POST.get('status')

            for application in applications:
                application.status = new_status
                application.save()

        return redirect('recruiter_applications')

    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@login_required
def add_company_details(request):
    try:
        if request.method == 'POST':
            form = CompanyProfileForm(request.POST)
            if form.is_valid():
                company_details = form.save(commit=False)
                company_details.created_by = request.user
                company_details.save()
                return redirect('view_company_details')  # Redirect to the appropriate page
        else:
            form = CompanyProfileForm()

        return render(request, 'add_company_details.html', {'form': form})

    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@login_required
def view_company_details(request):
    try:
        company_details = CompanyDetails.objects.filter(created_by=request.user)
        return render(request, 'company_details.html', {'company_details': company_details})

    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

