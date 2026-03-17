from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Application
from jobs.models import Job


@login_required
def apply_job(request, job_id):
    if not hasattr(request.user, 'studentprofile'):
        return redirect('dashboard')

    profile = request.user.studentprofile

    if not profile.phone or not profile.branch or not profile.skills:
        return redirect('update_profile')

    job = get_object_or_404(Job, id=job_id)

    if Application.objects.filter(student=request.user, job=job).exists():
        return redirect('my_applications')

    Application.objects.create(student=request.user, job=job)

    return redirect('my_applications')


@login_required
def my_applications(request):
    applications = Application.objects.filter(student=request.user)
    return render(request, 'applications/my_applications.html', {'applications': applications})


@login_required
def view_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Only company who posted job can view
    if job.company != request.user:
        return redirect('dashboard')

    applications = Application.objects.filter(job=job)

    return render(request, 'applications/view_applicants.html', {
        'applications': applications,
        'job': job
    })

@login_required
def update_status(request, app_id, status):
    application = get_object_or_404(Application, id=app_id)

    # Only company who posted job can update
    if application.job.company != request.user:
        return redirect('dashboard')

    if request.method == "POST":
        if status in ['selected', 'rejected']:
            application.status = status
            application.save()

    return redirect('view_applicants', job_id=application.job.id)

@login_required
def delete_application(request, app_id):
    application = get_object_or_404(Application, id=app_id)

    # Only student who applied can delete
    if application.student != request.user:
        return redirect('dashboard')

    if request.method == 'POST':
        application.delete()
        return redirect('my_applications')

    return render(request, 'applications/delete_application.html', {
        'application': application
    })