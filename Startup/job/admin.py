from django.contrib import admin
from .models import Job, JobApplications


class JobApplicationsAdmin(admin.ModelAdmin):
    list_display = ('job', 'jobSeeker', 'status')
    list_filter = ('status', 'job',)
    search_fields = ['job', 'jobSeeker', 'status', ]


class JobAdmin(admin.ModelAdmin):
    list_display = ('employer_id', 'title', 'requirements', 'type', 'Start_date', 'city', 'category', 'image')
    list_filter = ('employer_id', 'type', 'city', 'category',)
    search_fields = ['type', 'city', 'category', 'employer_id', ]
    date_hierarchy = 'Start_date'


admin.site.register(Job, JobAdmin)
admin.site.register(JobApplications, JobApplicationsAdmin)
