from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import (ChangePassword, ForgotPassword, Login, RegisterEmployer,
                    RegisterJobSeeker, RegisterView, ActiveAccountView,
                    get_cities,UserViewSetApiView,reSend_activeCode,logout_view,JobSeekerViewSetApiView,EmployerViewSetApiView)


router = DefaultRouter()
router.register('users',UserViewSetApiView)
router.register('employer',EmployerViewSetApiView)
router.register('jobseeker',JobSeekerViewSetApiView)

urlpatterns = [
    path('register',RegisterView.as_view(),name='register'),
    path('register-employer',RegisterEmployer.as_view(),name='register_employer'),
    path('register-jobseeker',RegisterJobSeeker.as_view(),name='register_jobseeker'),
    path('active-account',ActiveAccountView.as_view(),name='active_account'),
    path('forgot-password',ForgotPassword.as_view(),name='forgot_password'),
    # path('change-password/<verify_code>',ChangePassword.as_view(),name='change_password'),
    path('login',Login.as_view(),name='login'),
    path('logout',logout_view,name='logout'),
    path("get-cities", get_cities, name="get_cities"),
    path("resend-active-code", reSend_activeCode, name="reSend"),
    path("users/api/",include(router.urls)),
]
