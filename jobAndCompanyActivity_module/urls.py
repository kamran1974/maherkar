from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import JobViewSetApiView,CompanyActivityViewSetApiView

router = DefaultRouter()
router.register('job',JobViewSetApiView)
router.register('company',CompanyActivityViewSetApiView)


urlpatterns = [
    path('api/',include(router.urls))
]