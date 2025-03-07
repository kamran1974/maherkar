import jdatetime
from django.forms import widgets
from django.core.paginator import Paginator
from django.db.models import Case, IntegerField, Q, Value, When
from django.http import (HttpRequest, HttpResponse, HttpResponseNotFound,
                         JsonResponse)
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from iranian_cities.models import County

from account_module.models import User
from advertisement_module.models import Advertisment, Subscription,AdvertismentJobSeeker

from .forms import LocationForm, ReportModelForm


class HomeView(View):
    def get(self,request:HttpRequest):
        form = LocationForm()
        
        if request.user.is_authenticated and request.user.user_type == "employer":
            form.fields['county'].queryset = County.objects.filter(province = request.user.employer.province)
            form.fields['province'].widget = widgets.HiddenInput()
        
        now = jdatetime.datetime.now().replace(microsecond=0)
        advertisments = Advertisment.objects.filter(is_show = True,status = "approved",expire_date__gte=now).prefetch_related().order_by('-created_at')
        subscription=Subscription.objects.get(name = "نردبان")
        if request.user.is_authenticated:
            get_user = request.user
            get_user_type = get_user.user_type
            
                
            if get_user_type == "jobseeker":
                # advertisments = advertisments.filter(county = get_user.jobseeker.county)
                advertisments = advertisments.annotate(
                    near_by=Case(            
                        When (subscription = subscription,job =get_user.jobseeker.job_category  , then=Value(1)),
                        When (county = get_user.jobseeker.county,job =get_user.jobseeker.job_category  , then=Value(2)),
                        When (province = get_user.jobseeker.province,job =get_user.jobseeker.job_category  , then=Value(3)),
                        When (job =get_user.jobseeker.job_category  , then=Value(4)),
                        When (subscription = subscription, then=Value(5)),
                        When (county = get_user.jobseeker.county  , then=Value(6)),
                        When (province = get_user.jobseeker.province  , then=Value(7)),
                        default=Value(8),
                        output_field=IntegerField()
                    )
                ).order_by("near_by")
                
            elif get_user_type == "employer":
                advertisments = AdvertismentJobSeeker.objects.filter(province = get_user.employer.province,is_show = True,status = "approved",expire_date__gte=now)
                advertisments.annotate(
                    near_by=Case(
                        When(subscription = subscription,then=Value(1)),
                        default=Value(2),
                        output_field=IntegerField(),
                    )
                ).order_by("near_by")
                
            else:
                advertisments = advertisments.annotate(
                    near_by=Case(            
                        When (subscription = subscription,then=Value(1)),
                        default=Value(2),
                        output_field=IntegerField()
                    )
                ).order_by("near_by")
        else:
            advertisments = advertisments.annotate(
                    near_bt=Case(            
                        When (subscription = subscription,then=Value(1)),
                        default=Value(2),
                        output_field=IntegerField()
                    )
                ).order_by("near_bt")
        p = Paginator(advertisments,8)
        page_number = request.GET.get("page")
        page_obj = p.get_page(page_number)
        
        context = {'form':form , "advertisments" : page_obj}

        return render(request,"home_module/index.html",context)

    def post(self,request:HttpRequest):
        form = LocationForm(request.POST) 
        if request.user.is_authenticated and request.user.user_type == "employer":
            form.fields['county'].queryset = County.objects.filter(province = request.user.employer.province)
            form.fields['province'].widget = widgets.HiddenInput()
        query = Q()
        if form.is_valid():
            province = form.cleaned_data.get('province')
            county = form.cleaned_data.get('county')
            district = form.cleaned_data.get("district")
            job_type = form.cleaned_data.get('job_type')
            title = form.cleaned_data.get('search')
        
            if province:
                query &=Q(province__id=province.id)
            if county:
                query &=Q(county__id=county.id)
            if district:
                query &=Q(district__id=district.id)
            if job_type and job_type!="select":
                query &= Q(job_type=job_type)
            if title:
                query &=Q(title__icontains = title)
                
            now = jdatetime.datetime.now().replace(microsecond=0)

            if request.user.is_authenticated and request.user.user_type == "employer":
                advertisments = AdvertismentJobSeeker.objects.filter(query,is_show = True,status = "approved",expire_date__gte=now)
            else:    
                advertisments = Advertisment.objects.filter(query,is_show = True,status = "approved",expire_date__gte=now)
            
            p = Paginator(advertisments,8)
            page_number = request.GET.get("page")
            page_obj = p.get_page(page_number)
        
            context = {'form':form , "advertisments" : page_obj}
            return render(request,"home_module/index.html",context)


def advertisement_detail(request:HttpRequest,code):
    if request.user.is_authenticated:
        get_user = request.user
        if get_user.user_type == "employer":
            advertise = get_object_or_404(AdvertismentJobSeeker,advertise_code=code)
            jobseeker = advertise.jobSeeker
            province = advertise.province
            county = advertise.county
            district = advertise.district
            context = {'data':advertise,'jobseeker':jobseeker,'province':province,'county':county,'district':district}
            return render(request,'home_module/detail_jobseeker.html',context)
            

    advertise = get_object_or_404(Advertisment,advertise_code=code)
    employer = advertise.employer
    context = {'data':advertise,'employer':employer}
    return render(request,'home_module/detail.html',context)


class SendReport(View):
    def get(self,request,**kwargs):
        code = kwargs['code']
        if code:
            if request.user.is_authenticated:
                form = ReportModelForm()
                advertisement = get_object_or_404(Advertisment,advertise_code=code)
                
                context = {'form':form,'data':advertisement}
                return render(request,"home_module/report.html",context)
        
            else:
                return redirect('login')
        else:
            return HttpResponseNotFound('404')
    def post(self,request:HttpRequest,**kwargs):
        code = kwargs['code']
        if code:
            if request.user.is_authenticated:
                form = ReportModelForm(request.POST,request.FILES)
                if form.is_valid():
                    advertisement = get_object_or_404(Advertisment,advertise_code=code)
                    report = form.save(commit=False)
                    
                    report.user = request.user
                    report.advertisment = advertisement
                    report.save()
                    
                    return redirect('home')
                else:
                    context = {'form':form,'data':advertisement}
                    return render(request,"home_module/report.html",context)
        
            else:
                return redirect('login')
        else:
            return HttpResponseNotFound('404')

class SendReportJobSeeker(View):
    def get(self,request,**kwargs):
        code = kwargs['code']
        if code:
            if request.user.is_authenticated:
                form = ReportModelForm()
                advertisement = get_object_or_404(AdvertismentJobSeeker,advertise_code=code)
                
                context = {'form':form,'data':advertisement}
                return render(request,"home_module/report.html",context)
        
            else:
                return redirect('login')
        else:
            return HttpResponseNotFound('404')
    def post(self,request:HttpRequest,**kwargs):
        code = kwargs['code']
        if code:
            if request.user.is_authenticated:
                form = ReportModelForm(request.POST,request.FILES)
                if form.is_valid():
                    advertisement = get_object_or_404(AdvertismentJobSeeker,advertise_code=code)
                    report = form.save(commit=False)
                    
                    report.user = request.user
                    report.advertisment_jobSeeker = advertisement
                    report.save()
                    
                    return redirect('home')
                else:
                    context = {'form':form,'data':advertisement}
                    return render(request,"home_module/report.html",context)
        
            else:
                return redirect('login')
        else:
            return HttpResponseNotFound('404')
    


# ajax action
def get_cities(request:HttpRequest):
    province_id = int(request.GET.get('province_id'))
    try:
        cities = County.objects.filter(province_id=province_id).values("id", "name")
        return JsonResponse({"cities": list(cities)}, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
