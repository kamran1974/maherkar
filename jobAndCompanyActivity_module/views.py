from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from jobAndCompanyActivity_module.models import Job,CompanyActivity
from jobAndCompanyActivity_module.serializers import JobSerializer,CompanyActivitySerializer




class JobViewSetApiView(ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

class CompanyActivityViewSetApiView(ModelViewSet):
    queryset = CompanyActivity.objects.all()
    serializer_class = CompanyActivitySerializer