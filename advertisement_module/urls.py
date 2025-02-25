from django.urls import path,include
from .views import dashboard,CreateAdvertisement, get_cities,advetisement_list,delete_advertisement,advertisement_detail,UpdateAdvertisementView,AdvertismentModelViewSetApiView,DurationModelViewSetApiView,SkillModelViewSetApiView,SubscriptionModelViewSetApiView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("skill",SkillModelViewSetApiView)
router.register("duration",DurationModelViewSetApiView)
router.register("subscription",SubscriptionModelViewSetApiView)
router.register("advertisment",AdvertismentModelViewSetApiView)


urlpatterns = [
    path('',dashboard,name='dashboard'),
    path('manage',advetisement_list,name='advertisement_manage'),
    path('create',CreateAdvertisement.as_view(),name='create_advetisement'),
    path('update/<code>',UpdateAdvertisementView.as_view(),name='update_advetisement'),
    path('delete/<code>',delete_advertisement,name='delete_advetisement'),
    path('detail/<code>',advertisement_detail,name='detail_advetisement'),
    path("get-cities", get_cities, name="get_cities"),
    path("api/",include(router.urls))

]