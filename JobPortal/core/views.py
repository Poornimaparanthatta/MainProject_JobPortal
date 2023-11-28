from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from account.models import User
from recruiter.models import JobPost
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

def index(request):
    try:
        return render(request, 'index.html')

    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    job_seekers = User.objects.filter(usertype='Job Seeker')
    recruiters = JobPost.objects.values('created_by').distinct()

    recruiter_details = JobPost.objects.filter(created_by__in=recruiters)

    context = {'job_seekers': job_seekers, 'recruiters': recruiter_details}

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'delete_recruiter':
            recruiter_username = request.POST.get('recruiter_username')
            recruiter = get_object_or_404(User, username=recruiter_username)
            recruiter.delete()

    return render(request, 'admin_dashboard.html', context)

@login_required
def dashboard(request):
    try:
        user = request.user

        if not user.is_authenticated or not user.is_job_seeker:
            return redirect('index')

        try:
            user_profile = User.objects.get(username=user.username)
        except User.DoesNotExist:
            raise Exception("User profile not found")

        return render(request, 'dashboard.html', {'user_profile': user_profile})

    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})