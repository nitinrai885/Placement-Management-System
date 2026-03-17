from django.urls import path
from . import views

urlpatterns = [
    path('create-job/', views.create_job, name='create_job'),
    path('jobs/', views.job_list, name='job_list'),
    path('company-jobs/', views.company_jobs, name='company_jobs'),
    path('edit-job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('delete-job/<int:job_id>/', views.delete_job, name='delete_job'),
]