from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.job_list_api, name='job_list_api'),
    path('applications/', views.application_list_api, name='application_list_api'),
    path('students/', views.student_list_api, name='student_list_api'),
]