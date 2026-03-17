from rest_framework.decorators import api_view
from rest_framework.response import Response
from jobs.models import Job
from applications.models import Application
from django.contrib.auth.models import User
from .serializers import JobSerializer, ApplicationSerializer, UserSerializer


@api_view(['GET'])
def job_list_api(request):
    jobs = Job.objects.all()
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def application_list_api(request):
    applications = Application.objects.all()
    serializer = ApplicationSerializer(applications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def student_list_api(request):
    students = User.objects.all()
    serializer = UserSerializer(students, many=True)
    return Response(serializer.data)