from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import User, Employer, JobSeeker


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'is_employer']


class JobSeekerSignUpSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        if validated_data['password'] != validated_data['confirm_password']:
            raise serializers.ValidationError({"error": "Not matched"})
        else:
            user.set_password(validated_data['password'])
            user.is_jobSeeker = True
            user.save()
            group = Group.objects.get(name='jobSeekers_editors')
            group.user_set.add(user)
            JobSeeker.objects.create(user=user)
            return user


class EmployerSignUpSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        if validated_data['password'] != validated_data['confirm_password']:
            raise serializers.ValidationError({"error": "Not matched"})
        else:
            user.set_password(validated_data['password'])
            user.is_employer = True
            user.save()
            group = Group.objects.get(name='employers_editors')
            group.user_set.add(user)
            Employer.objects.create(user=user)
            return user


class JobSeekerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = JobSeeker
        fields = '__all__'
        depth = 1
