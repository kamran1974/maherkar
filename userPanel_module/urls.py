from django.urls import path
from .views import user_dashboard,UpdateUserView,UpdateUserPasswordView,UpdateEmployerView,UpdateJobSeekerView



urlpatterns = [
    path('',user_dashboard,name = 'user_dashboard'),
    path("update-user",UpdateUserView.as_view(),name='update_user'),
    path("update-password",UpdateUserPasswordView.as_view(),name='update_password'),
    path("update-employer",UpdateEmployerView.as_view(),name='update_employer'),
    path("update-jobseeker",UpdateJobSeekerView.as_view(),name='update_jobseeker'),
]