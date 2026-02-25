from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Job
from .forms import JobForm


@login_required
def create_job(request):
    # Only company can post
    if not hasattr(request.user, 'companyprofile'):
        return redirect('dashboard')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user
            job.save()
            return redirect('company_jobs')
    else:
        form = JobForm()

    return render(request, 'jobs/create_job.html', {'form': form})


@login_required
def job_list(request):
    query = request.GET.get('q')
    jobs = Job.objects.all()

    if query:
        jobs = jobs.filter(title__icontains=query)

    return render(request, 'jobs/job_list.html', {'jobs': jobs})

@login_required
def company_jobs(request):
    jobs = Job.objects.filter(company=request.user)
    return render(request, 'jobs/company_jobs.html', {'jobs': jobs})


from django.shortcuts import get_object_or_404

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Only company who posted can edit
    if job.company != request.user:
        return redirect('dashboard')

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('company_jobs')
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/edit_job.html', {'form': form})

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if job.company != request.user:
        return redirect('dashboard')
    if request.method == 'POST':
        job.delete()
        return redirect('company_jobs')
    return render(request, 'jobs/delete_job.html', {'job': job})