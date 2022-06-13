from django.contrib import admin
from .models import User, Employer, JobSeeker


# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(User, ProfileAdmin)
admin.site.register(Employer)
admin.site.register(JobSeeker)
