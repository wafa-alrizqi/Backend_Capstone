from . import permissions
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serializers import UserSerializer, EmployerSignUpSerializer, JobSeekerSignUpSerializer, JobSeekerSerializer, \
    EmployerSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import Employer, JobSeeker


# Create your views here.


class EmployerSignUpView(generics.GenericAPIView):
    """
    Employer Sign up
    """
    serializer_class = EmployerSignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "msg": "account created successfully"
        })


class JobSeekerSignUpView(generics.GenericAPIView):
    """
    Job Seeker Sign up
    """
    serializer_class = JobSeekerSignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "msg": "account created successfully"
        })


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'is_employer': user.is_employer
        })


@api_view(['POST'])
def login_user(request: Request):
    """
    login for employer and job seeker
    """

    if 'username' in request.data and 'password' in request.data:
        user = authenticate(request, username=request.data['username'], password=request.data['password'])
        if user is not None:
            token = AccessToken.for_user(user)
            responseData = {
                "user": user.id,
                'msg': 'Your token is ready',
                'token': str(token)
            }
            return Response(responseData)
    return Response({'msg': 'Provide your username and password'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request: Request, format=None):
        request.user.auth.delete()
        return Response({"msg": "You are Logged Out"}, status=status.HTTP_200_OK)


class EmployerOnlyView(generics.RetrieveAPIView):
    """
    just a dashboard for employer
    """
    permission_classes = [permissions.isEmployerUser]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class JobSeekerOnlyView(generics.RetrieveAPIView):
    """
    just a dashboard for job seeker
    """
    permission_classes = [permissions.isJobSeekerUser]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_profile_JobSeeker(request: Request, jobSeeker_id):
    if not request.user.is_authenticated:
        return Response({'msg': 'Not Allowed'}, status=status.HTTP_401_UNAUTHORIZED)

    jobSeeker = JobSeeker.objects.get(id=jobSeeker_id)
    if request.user.id == jobSeeker.user.id:
        profile_updated = JobSeekerSerializer(instance=jobSeeker, data=request.data)
        request.data['user'] = request.user.id
        if profile_updated.is_valid():
            profile_updated.save()
            responseData = {
                'msg': 'Profile Updated Successfully',
                'User Profile': JobSeekerSerializer(instance=jobSeeker).data
            }
            return Response(responseData, status=status.HTTP_200_OK)
        else:
            return Response(profile_updated.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'msg': 'Not Unauthorized User'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def view_profile_JobSeeker(request: Request, jobSeeker_id):
    if not request.user.is_authenticated:
        return Response({'msg': 'Not Allowed'}, status=status.HTTP_401_UNAUTHORIZED)

    jobSeeker = JobSeeker.objects.get(id=jobSeeker_id)
    if request.user.id == jobSeeker.user.id:
        request.data['user'] = request.user.id
        dataResponse = {
            'msg': 'Job Seeker Profile',
            'Profile': JobSeekerSerializer(instance=jobSeeker).data
        }
        return Response(dataResponse)
    else:
        return Response({'msg': 'Not Unauthorized User'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_profile_employer(request: Request, employer_id):
    if not request.user.is_authenticated:
        return Response({'msg': 'Not Allowed'}, status=status.HTTP_401_UNAUTHORIZED)

    employer = Employer.objects.get(id=employer_id)
    if request.user.id == employer.user.id:
        profile_updated = EmployerSerializer(instance=employer, data=request.data)
        request.data['user'] = request.user.id
        if profile_updated.is_valid():
            profile_updated.save()
            responseData = {
                'msg': 'Profile Updated Successfully',
                'User Profile': EmployerSerializer(instance=employer).data
            }
            return Response(responseData, status=status.HTTP_200_OK)
        else:
            return Response(profile_updated.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'msg': 'Not Unauthorized User'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def view_profile_employer(request: Request, employer_id):
    if not request.user.is_authenticated:
        return Response({'msg': 'Not Allowed'}, status=status.HTTP_401_UNAUTHORIZED)

    employer = Employer.objects.get(id=employer_id)
    if request.user.id == employer.user.id:
        request.data['user'] = request.user.id
        dataResponse = {
            'msg': 'Employer Profile',
            'Profile': EmployerSerializer(instance=employer).data
        }
        return Response(dataResponse)
    else:
        return Response({'msg': 'Not Unauthorized User'}, status=status.HTTP_401_UNAUTHORIZED)

