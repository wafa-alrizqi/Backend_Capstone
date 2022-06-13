from django.db import models
from django.contrib.auth.models import AbstractUser

#  Create your models here.


class User(AbstractUser):
    is_employer = models.BooleanField(default=False)
    is_jobSeeker = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Employer(models.Model):
    user = models.OneToOneField(User, related_name='employer', on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, null=True, blank=True)
    brief = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class JobSeeker(models.Model):
    user = models.OneToOneField(User, related_name='jobSeeker', on_delete=models.CASCADE)
    phone = models.CharField(max_length=120, null=True, blank=True)
    cv = models.URLField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.user.username


