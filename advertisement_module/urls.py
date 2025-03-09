from django.urls import include, path
from rest_framework.routers import DefaultRouter

# ایمپورت ویوهای مورد نیاز
from .views import (
    AdvertisementModelViewSetApiView,
    CreateAdvertisement,
    CreateJobHistory,
    AdDisplayDurationModelViewSetApiView,
    JobSeekerCreateAdvertisement,
    JobSeekerUpdateAdvertisementView,
    SkillModelViewSetApiView,
    SubscriptionModelViewSetApiView,
    UpdateAdvertisementView,
    JobHistoryViewSetApiView,
    AdvertisementJobSeekerModelViewSetApiView,
    UpdateJobHistory,
    advertisement_detail,
    advertisement_list,
    dashboard,
    delete_advertisement,
    delete_job_history,
    delete_job_seeker_advertisement,
    get_cities,
    job_histories,
    job_seeker_advertisement_list,
    job_seeker_advertisement_detail
)

# تنظیم router برای API ها
router = DefaultRouter()
router.register("skill", SkillModelViewSetApiView)
router.register("duration", AdDisplayDurationModelViewSetApiView)
router.register("job-history", JobHistoryViewSetApiView)
router.register("subscription", SubscriptionModelViewSetApiView)
router.register("advertisement", AdvertisementModelViewSetApiView)
router.register("jobseeker/advertisement", AdvertisementJobSeekerModelViewSetApiView)

# تنظیم الگوهای URL
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('manage', advertisement_list, name='advertisement_manage'),
    path('create', CreateAdvertisement.as_view(), name='create_advertisement'),
    path('update/<code>', UpdateAdvertisementView.as_view(), name='update_advertisement'),
    path('delete/<code>', delete_advertisement, name='delete_advertisement'),
    path('detail/<code>', advertisement_detail, name='detail_advertisement'),
    
    path("jobseeker/manage", job_seeker_advertisement_list, name='jobseeker_manage'),
    path('jobseeker/detail/<code>', job_seeker_advertisement_detail, name='jobseeker_detail_advertisement'),
    path('jobseeker/create', JobSeekerCreateAdvertisement.as_view(), name='jobseeker_create_advertisement'),
    path('jobseeker/update/<code>', JobSeekerUpdateAdvertisementView.as_view(), name='jobseeker_update_advertisement'),
    path('jobseeker/delete/<code>', delete_job_seeker_advertisement, name='jobseeker_delete_advertisement'),
    
    path("job_histories", job_histories, name='job_histories'),
    path('job-history/create', CreateJobHistory.as_view(), name='create_history'),
    path('job-history/update/<code>', UpdateJobHistory.as_view(), name='update_history'),
    path('job-history/delete/<code>', delete_job_history, name='delete_history'),
    
    path("get-cities", get_cities, name="get_cities"),
    path("api/", include(router.urls))
]
