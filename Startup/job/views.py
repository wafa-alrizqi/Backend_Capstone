from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, generics, serializers
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Job, JobApplications
from .serializers import JobSerializer, JobApplicationsSerializer

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()


# Job CRUD functions
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def add_job(request: Request):
    if not request.user.is_authenticated and not request.user.is_employer:
        print(request.user.is_employer)
        return Response({'msg': 'Not Allowed!'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        job = JobSerializer(data=request.data)
        if job.is_valid() and request.user.is_employer:
            job.save()
            dataResponse = {
                'msg': 'Job Added Successfully',
                'job': job.data
            }
            return Response(dataResponse)
        else:
            print(job.errors)
            dataResponse = {'msg': 'Unable to add job'}
            return Response(dataResponse, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def all_jobs(request: Request):
    job = Job.objects.all()
    dataResponse = {
        'msg': 'List of All Jobs',
        'Job': JobSerializer(instance=job, many=True).data
    }
    return Response(dataResponse)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_job(request: Request, job_id):
    if not request.user.is_authenticated:
        return Response({'msg': 'Not Allowed'}, status=status.HTTP_401_UNAUTHORIZED)

    job = Job.objects.get(id=job_id)
    print(job.employer_id.user.id)
    print(request.user.id)
    if request.user.id == job.employer_id.user.id:
        job_updated = JobSerializer(instance=job, data=request.data)
        if job_updated.is_valid():
            job_updated.save()
            responseData = {'msg': 'Job Updated Successfully'}
            return Response(responseData)
    else:
        return Response({'msg': 'Not Unauthorized User'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@login_required
def delete_job(request: Request, job_id):
    if not request.user.is_authenticated and not request.user.is_employer:
        return Response({'msg': 'Not Allowed'}, status=status.HTTP_401_UNAUTHORIZED)
    job = Job.objects.get(id=job_id)
    print(job.employer_id.user.id)
    print(request.user.id)
    if request.user.id == job.employer_id.user.id:
        job.delete()
        return Response({'msg': 'Job Deleted Successfully'})
    else:
        return Response({'msg': 'Not Unauthorized User'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def posted_jobs_per_employer(request: Request, employer_id):
    # username = User.objects.get(id=request.user.id)
    # print(username)
    # if username.is_employer:
    #     print(username)
    job = Job.objects.filter(employer_id=employer_id)
    dataResponse = {
        'msg': 'List of All Jobs',
        'Job': JobSerializer(instance=job, many=True).data
    }
    return Response(dataResponse)


# Job Applications CRUD functions

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def apply_for_job(request: Request):
    if not request.user.is_authenticated and not request.user.is_jobSeeker:
        print(request.user.is_employer)
        return Response({'msg': 'Not Allowed!'}, status=status.HTTP_401_UNAUTHORIZED)

    else:
        application = JobApplicationsSerializer(data=request.data)
        print(request.user.id)

        if application.is_valid() and request.user.is_jobSeeker:
            application.save()
            dataResponse = {
                'msg': 'Applied Successfully',
                'application': application.data
            }
            return Response(dataResponse)
        else:
            print(application.errors)
            dataResponse = {'msg': 'Unable to Apply'}
            return Response(dataResponse, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_application(request: Request, application_id):
    if not request.user.is_authenticated and not request.user.is_jobSeeker:
        return Response({'msg': 'Not Allowed'}, status=status.HTTP_401_UNAUTHORIZED)
    application = JobApplications.objects.get(id=application_id)
    print(application.jobSeeker.user.id)
    print(request.user.id)
    if request.user.id == application.jobSeeker.user.id:
        application.delete()
        return Response({'msg': 'Job Deleted Successfully'})
    else:
        return Response({'msg': 'Not Unauthorized User'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def applied_job_list(request: Request, jobSeeker_id):
    """
    get list of applied jobs for each job seeker
    """
    if request.user.is_authenticated:
        application = JobApplications.objects.filter(jobSeeker=jobSeeker_id)
        dataResponse = {
            'msg': 'List of My Applied Jobs',
            'Job': JobApplicationsSerializer(instance=application, many=True).data
        }
        return Response(dataResponse)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def applications_per_job(request: Request, employer_id):
    print(request.user.id)
    application = JobApplications.objects.all()
    dataResponse = {
        'msg application': 'List of Applied Jobs',
        'application': JobApplicationsSerializer(instance=application, many=True).data
    }
    return Response(dataResponse)


