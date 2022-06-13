from . import permissions
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serializers import UserSerializer, EmployerSignUpSerializer, JobSeekerSignUpSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate

from .models import User
# Create your views here.


class EmployerSignUpView(generics.GenericAPIView):
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
    def post(self, request, format=None):
        request.auth.delete()
        return Response({"msg": "You are Logged Out"}, status=status.HTTP_200_OK)


class EmployerOnlyView(generics.RetrieveAPIView):
    permission_classes = [permissions.isEmployerUser]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class JobSeekerOnlyView(generics.RetrieveAPIView):
    permission_classes = [permissions.isJobSeekerUser]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
