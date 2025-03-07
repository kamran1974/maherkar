from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AdvertismentModelViewSetApiView, CreateAdvertisement,
                    CreateJobHistory, DurationModelViewSetApiView,
                    JobSeekerCreateAdvertisement,
                    JobSeekerUpdateAdvertisementView, SkillModelViewSetApiView,
                    SubscriptionModelViewSetApiView, UpdateAdvertisementView,JobHistoryViewSetApiView,AdvertismentJobSeekerModelViewSetApiView,
                    UpdateJobHistory, advertisement_detail, advetisement_list,
                    dashboard, delete_advertisement, delete_jobHistory,
                    delete_jobseeker_advertisement, get_cities, job_histories,
                    jobSeeker_advetisement_list,jobseeker_advertisement_detail)

router = DefaultRouter()

router.register("skill",SkillModelViewSetApiView)
router.register("duration",DurationModelViewSetApiView)
router.register("job-history",JobHistoryViewSetApiView)
router.register("subscription",SubscriptionModelViewSetApiView)
router.register("advertisment",AdvertismentModelViewSetApiView)
router.register("jobseeker/advertisment",AdvertismentJobSeekerModelViewSetApiView)


urlpatterns = [
    path('',dashboard,name='dashboard'),
    path('manage',advetisement_list,name='advertisement_manage'),
    path('create',CreateAdvertisement.as_view(),name='create_advetisement'),
    path('update/<code>',UpdateAdvertisementView.as_view(),name='update_advetisement'),
    path('delete/<code>',delete_advertisement,name='delete_advetisement'),
    path('detail/<code>',advertisement_detail,name='detail_advetisement'),
    
    path("jobseeker/manage",jobSeeker_advetisement_list,name='jobseeker_manage'),
    path('jobseeker/detail/<code>',jobseeker_advertisement_detail,name='jobseeker_detail_advetisement'),
    path('jobseeker/create',JobSeekerCreateAdvertisement.as_view(),name='jobseeker_create_advetisement'),
    path('jobseeker/update/<code>',JobSeekerUpdateAdvertisementView.as_view(),name='jobseeker_update_advetisement'),
    path('jobseeker/delete/<code>',delete_jobseeker_advertisement,name='jobseeker_delete_advetisement'),
    
    path("job_histories",job_histories,name='job_histories'),
    path('job-history/create',CreateJobHistory.as_view(),name='create_history'),
    path('job-history/update/<code>',UpdateJobHistory.as_view(),name='update_history'),
    path('job-history/delete/<code>',delete_jobHistory,name='delete_history'),
    
    path("get-cities", get_cities, name="get_cities"),
    path("api/",include(router.urls))

]