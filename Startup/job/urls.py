from django.urls import path
from . import views

app_name = 'job'
urlpatterns = [
    # End points for job model
    path('add_job/', views.add_job, name='add_job'),
    path('all_jobs/', views.all_jobs, name='all_jobs'),
    path('update_job/<job_id>/', views.update_job, name='update_job'),
    path('delete_job/<job_id>/', views.delete_job, name='delete_job'),
    path('posted_jobs_per_employer/<employer_id>/', views.posted_jobs_per_employer, name='posted_jobs_per_employer'),

    # End points for job application model
    path('apply_for_job/', views.apply_for_job, name='apply_for_job'),
    path('delete_application/<application_id>/', views.delete_application, name='delete_application'),
    path('applied_job_list/<jobSeeker_id>/', views.applied_job_list, name='applied_job_list'),
    path('applications_per_job/<employer_id>/', views.applications_per_job, name='applications_per_job'),

]
