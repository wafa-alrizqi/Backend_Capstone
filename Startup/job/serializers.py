from rest_framework import serializers
from .models import Job, JobApplications


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class JobApplicationsSerializer(serializers.ModelSerializer):
    job_title = serializers.ReadOnlyField(source='job.title')
    job_seeker_name = serializers.ReadOnlyField(source='jobSeeker.user.username')
    job = JobSerializer()

    class Meta:
        model = JobApplications
        fields = ('job', 'jobSeeker', 'status', 'job_title', 'job_seeker_name')
        depth = 1


class Applications_Status_Serializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplications
        fields = ['status']
