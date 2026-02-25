from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegisterForm, StudentProfileForm, CompanyProfileForm
from .models import StudentProfile, CompanyProfile
from django.contrib.auth.decorators import login_required



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')

            if role == 'student':
                StudentProfile.objects.create(user=user)
            else:
                CompanyProfile.objects.create(user=user)

            login(request, user)
            if role == 'student':
                return redirect('update_profile')
            else:
                return redirect('dashboard')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print("USERNAME:", username)
        print("PASSWORD:", password)

        user = authenticate(request, username=username, password=password)

        print("USER OBJECT:", user)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'users/login.html', {
                'error': 'Invalid credentials'
            })

    return render(request, 'users/login.html')
def user_logout(request):
    logout(request)
    return redirect('login')


def dashboard(request):

    if hasattr(request.user, 'studentprofile'):
        profile = request.user.studentprofile

        # Check if profile incomplete
        if not profile.phone or not profile.branch or not profile.skills:
            return redirect('update_profile')

        return render(request, 'users/student_dashboard.html')

    elif hasattr(request.user, 'companyprofile'):
        return render(request, 'users/company_dashboard.html')

    return redirect('login')


@login_required
def update_profile(request):
    profile = request.user.studentprofile

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = StudentProfileForm(instance=profile)

    return render(request, 'users/update_profile.html', {'form': form})