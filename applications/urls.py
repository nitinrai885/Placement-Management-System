from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('applicants/<int:job_id>/', views.view_applicants, name='view_applicants'),
    path('update-status/<int:app_id>/<str:status>/', views.update_status, name='update_status'),
    path('delete-application/<int:app_id>/', views.delete_application, name='delete_application'),
]