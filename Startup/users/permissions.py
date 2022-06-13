from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group, Permission


class isEmployerUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_employer)


class isJobSeekerUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_jobSeeker)

