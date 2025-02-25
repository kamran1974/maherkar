from django.http import HttpRequest, HttpResponseNotFound, JsonResponse,Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from iranian_cities.models import County
from rest_framework.viewsets import ModelViewSet

from account_module.models import Employer
from advertisement_module.models import (Advertisment, Duration, Skill,
                                         Subscription)
from advertisement_module.serializers import (AdvertisementModelSerializer,
                                              DurationModelSerializer,
                                              SkillModelSerializer,
                                              SubscriptionModelSerializer)

from .forms import AdvertisementModelForm, UpdateAdvertisementModelForm,ReportAdvertisment


def check_employer(request:HttpRequest):
    if request.user.is_authenticated:
        get_user = request.user
        if get_user.user_type == "employer":
            return True
        else:
            False
    else:
        False
def check_verified_by_admin(request):
    if request.user.is_authenticated:
        get_user = request.user
        if get_user.user_type == "employer":
            if get_user.employer.verified_by_admin:
                return True
            else:
                False
        else:
            False
    else:
        False
    

def dashboard(request:HttpRequest):
    if check_employer(request):
        get_user_name = request.user.first_name
        check_verified_by_admin = request.user.employer.verified_by_admin
        
        status = False
        if check_verified_by_admin:
            status = True
        else:
            False
        
        context = {'name':get_user_name,'status':status}
        return render(request,'advertisement_module/home.html',context)
    return HttpResponseNotFound("404")


def advetisement_list(request):
    if check_verified_by_admin(request):
        get_employer = request.user.employer
        
        
        advertisements = Advertisment.objects.filter(employer = get_employer).order_by('created_at')
        
        context = {'advertisements' : advertisements}
        
        return render(request,"advertisement_module/manage.html",context)
        
    return HttpResponseNotFound("404")


def advertisement_detail(request,code):
    if check_verified_by_admin(request) and code:
        advertise = get_object_or_404(Advertisment,advertise_code=code)
        get_employer = advertise.employer
        
        context = {'data':advertise,'province':get_employer.province,'county':get_employer.county,'district':get_employer.district}
        return render(request,'advertisement_module/detail.html',context)
    return HttpResponseNotFound("404")
        

class CreateAdvertisement(View):
    def get(self,request,**kwargs):
        if check_verified_by_admin(request):
            form =  AdvertisementModelForm()
            context = {'form':form}
            return render(request,"advertisement_module/create.html",context)
        return HttpResponseNotFound("404")

    def post(self,request):
        if check_verified_by_admin(request):
            form = AdvertisementModelForm(request.POST)
            if form.is_valid():
                
                get_employer = request.user.employer
                
                advertise = form.save(commit=False)
                
                advertise.province = get_employer.province
                
                advertise.county = get_employer.county
                
                if get_employer.district:
                    advertise.district = get_employer.district
                                
                advertise.employer = get_employer
                
                advertise.save()
                
                return redirect("dashboard")
            else:
                context ={'form':form}
                return render(request,"advertisement_module/create.html",context)
        return HttpResponseNotFound("404")

class UpdateAdvertisementView(View):
    def get(self,request,**kwargs):
        if check_verified_by_admin(request):
            code = kwargs.get('code')
            if code:
                advertise = get_object_or_404(Advertisment,advertise_code=code)
                form = UpdateAdvertisementModelForm(instance=advertise)
                form.advertise_code = code
            
                context = {'form':form}
                return render(request,"advertisement_module/update.html",context)
            else:
                return HttpResponseNotFound("404")
        else:
            return HttpResponseNotFound("404")
        
    def post(self,request,**kwargs):
        if check_verified_by_admin(request):

            code = kwargs.get('code')
            if code:
                advertise = get_object_or_404(Advertisment,advertise_code=code)
                advertise_form_instance = get_object_or_404(Advertisment,advertise_code=code)
                form = UpdateAdvertisementModelForm(request.POST,instance=advertise_form_instance)
                if form.is_valid():
                    advertise_form = form.save(commit=False)
                    advertise_form.advertise_code = code
                    advertise_form.is_show = False
                    advertise_form.check_by_admin = False
                    advertise_form.status = 'pending'
                    if advertise_form.duration_id!= advertise.duration_id or advertise_form.subscription_id != advertise.subscription_id:
                        duration = 0
                        subscription = 0
                        if advertise_form.duration_id != advertise.duration_id:
                            duration = Duration.objects.get(pk = advertise_form.duration_id).price
                        if advertise_form.subscription_id != advertise.subscription_id:
                            subscription = Subscription.objects.get(pk=advertise_form.subscription_id).price
                        sum = int(duration) + int(subscription)
                        advertise_form.total_price = sum
                        if advertise_form.total_price >0:
                            advertise_form.pay_status = False
                            advertise_form.status = "unpaid"
                
                    advertise_form.save()
                    return redirect("advertisement_manage")
                else:
                    context = {'form':form}
                    return render(request,"advertisement_module/update.html",context)
            return HttpResponseNotFound("404")
        else:
            return HttpResponseNotFound("404")

                
        
        
def delete_advertisement(request,code):
    if check_verified_by_admin(request) and code:
        advertise = get_object_or_404(Advertisment,advertise_code=code)
        advertise.delete()
        
        return redirect('advertisement_manage')
    return HttpResponseNotFound("404")

  
# API


class SubscriptionModelViewSetApiView(ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionModelSerializer

class SkillModelViewSetApiView(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillModelSerializer

class DurationModelViewSetApiView(ModelViewSet):
    queryset = Duration.objects.all()
    serializer_class = DurationModelSerializer

class AdvertismentModelViewSetApiView(ModelViewSet):
    queryset = Advertisment.objects.all().order_by('-created_at')
    serializer_class = AdvertisementModelSerializer
  

    
# ajax action
def get_cities(request:HttpRequest):
    province_id = int(request.GET.get('province_id'))
    try:
        cities = County.objects.filter(province_id=province_id).values("id", "name")
        return JsonResponse({"cities": list(cities)}, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)