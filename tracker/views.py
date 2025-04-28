from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView


from .forms import RegisterForm, JobApplicationForm
from .models import JobApplication

from django.core.paginator import Paginator
from datetime import date, timedelta

from django.core.mail import send_mail

@login_required
def dashboard(request):
    return render(request, "dashboard.html")

@login_required
def job_list(request):
    jobs = JobApplication.objects.filter(user=request.user)

    # Get search query
    search_query = request.GET.get("q", "")
    if search_query:
        jobs = jobs.filter(company_name__icontains=search_query)  # Case-insensitive search

    # Get filter option
    status_filter = request.GET.get("status", "")
    if status_filter:
        jobs = jobs.filter(status=status_filter)

    # Filtering for urgent jobs (deadlines within 3 days)
    urgent_filter = request.GET.get("urgent")
    if urgent_filter == "1":
        today = date.today()
        urgent_deadline = today + timedelta(days=3)
        jobs = jobs.filter(deadline__lte=urgent_deadline)  # ✅ Apply filtering on QuerySet

    # Pagination: Show 5 jobs per page
    paginator = Paginator(jobs, 5)
    page_number = request.GET.get("page")
    jobs = paginator.get_page(page_number)




    return render(request, "tracker/job_list.html", {"jobs": jobs, "search_query": search_query,
        "status_filter": status_filter,"urgent_filter": urgent_filter,})

@login_required
def add_job(request):
    if request.method == "POST":
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.save()
            return redirect("job_list")
    else:
        form = JobApplicationForm()
    return render(request, "tracker/job_form.html", {"form": form})

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(JobApplication, id=job_id, user=request.user)
    if request.method == "POST":
        form = JobApplicationForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect("job_list")
    else:
        form = JobApplicationForm(instance=job)
    return render(request, "tracker/job_form.html", {"form": form})

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(JobApplication, id=job_id, user=request.user)
    if request.method == "POST":
        job.delete()
        return redirect("job_list")
    return render(request, "tracker/job_confirm_delete.html", {"job": job})

class CustomLoginView(LoginView):
    template_name = "login.html"

class CustomLogoutView(LogoutView):
    next_page = "login"

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})




def urgent_jobs(request):
    selected_filter = request.GET.get('deadline_filter', 'upcoming')  # default: no filter

    if selected_filter == 'today':
        jobs = JobApplication.objects.filter(
            user=request.user,
            deadline=date.today()
        )
    elif selected_filter == 'overdue':
        jobs = JobApplication.objects.filter(
            user=request.user,
            deadline__lt=date.today()
        )
    else :
        # selected_filter == 'upcoming'):
        jobs = JobApplication.objects.filter(
            user=request.user,
            deadline__gte=date.today(),
            deadline__lte=date.today() + timedelta(days=3)
        )


    # Pagination: Show 5 jobs per page
    paginator = Paginator(jobs, 5)
    page_number = request.GET.get("page")
    jobs = paginator.get_page(page_number)

    return render(request, 'tracker/deadline_jobs.html', {
        'jobs': jobs,
        'selected_filter': selected_filter
    })


