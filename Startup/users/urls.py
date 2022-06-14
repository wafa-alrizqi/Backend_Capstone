from django.urls import path
from .views import JobSeekerSignUpView, EmployerSignUpView, CustomAuthToken, LogoutView, EmployerOnlyView, \
    JobSeekerOnlyView
from . import views

app_name = 'users'
# All The End Points associated with Employer and Job Seeker
urlpatterns = [
    path('employer/', EmployerSignUpView.as_view()),
    path('jobSeeker/', JobSeekerSignUpView.as_view()),
    path('login/', views.login_user, name='login_user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('employer/dashboard/', EmployerOnlyView.as_view(), name='employer_dashboard'),
    path('jobSeeker/dashboard/', JobSeekerOnlyView.as_view(), name='jobSeeker_dashboard'),
    path('update_profile_JobSeeker/<jobSeeker_id>/', views.update_profile_JobSeeker, name='update_profile_JobSeeker'),
    path('view_profile_JobSeeker/<jobSeeker_id>/', views.view_profile_JobSeeker, name='view_profile_JobSeeker'),
    path('update_profile_employer/<employer_id>/', views.update_profile_employer, name='update_profile_employer'),
    path('view_profile_employer/<employer_id>/', views.view_profile_employer, name='view_profile_employer'),

]
