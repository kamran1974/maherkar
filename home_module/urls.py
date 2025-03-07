from django.urls import path
from .views import HomeView, advertisement_detail, get_cities,SendReport,SendReportJobSeeker


urlpatterns = [
    path('',HomeView.as_view(),name="home"),
    path('detail/<code>',advertisement_detail,name='detail_advetisement_home'),
    path('report/<code>',SendReport.as_view(),name='report'),
    path('jobseeker/report/<code>',SendReportJobSeeker.as_view(),name='report_jobseeker'),

    path("get-cities", get_cities),
]