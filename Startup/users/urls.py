from django.urls import path
from .views import JobSeekerSignUpView, EmployerSignUpView, CustomAuthToken,LogoutView, EmployerOnlyView, JobSeekerOnlyView
from . import views

app_name = 'users'
urlpatterns = [
    path('employer/', EmployerSignUpView.as_view()),
    path('jobSeeker/', JobSeekerSignUpView.as_view()),
    path('login/', views.login_user, name='login_user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('employer/dashboard/', EmployerOnlyView.as_view(), name='employer_dashboard'),
    path('jobSeeker/dashboard/', JobSeekerOnlyView.as_view(), name='jobSeeker_dashboard')

]
