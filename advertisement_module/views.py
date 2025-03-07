from django.http import (Http404, HttpRequest, HttpResponse,
                         HttpResponseNotFound, JsonResponse)
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from iranian_cities.models import County
from rest_framework.viewsets import ModelViewSet

from account_module.models import Employer
from advertisement_module.models import (Advertisment, AdvertismentJobSeeker,
                                         Duration, JobHistory, Skill,
                                         Subscription)
from advertisement_module.serializers import (AdvertisementModelSerializer,
                                              DurationModelSerializer,
                                              SkillModelSerializer,
                                              SubscriptionModelSerializer,JobHistoryModelSerializer,AdvertisementJobSeekerModelSerializer)

from .forms import (AdvertisementModelForm, JobHistoryModelForm,
                    JobSeekerAdvertisementModelForm, ReportAdvertisment,
                    UpdateAdvertisementModelForm)

# region function

def check_employer(request:HttpRequest):
    if request.user.is_authenticated:
        get_user = request.user
        if get_user.user_type == "employer":
            return True
        else:
            False
    else:
        False

def check_jobSeeker(request:HttpRequest):
    if request.user.is_authenticated:
        get_user = request.user
        if get_user.user_type == "jobseeker":
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
        elif get_user.user_type == "jobseeker":
            return True
    else:
        False

#endregion

#region advetisement

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
                form.save_m2m()
                
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
                    form.save_m2m()
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

# endregion

# region jobseeker

def jobSeeker_advetisement_list(request):
    if check_jobSeeker(request):
        try:
            advertisment = AdvertismentJobSeeker.objects.get(jobSeeker = request.user.jobseeker)
        except:
            advertisment = None
        
        get_jobseeker = request.user.jobseeker
            
        jobs = get_jobseeker.job_histories.all()
        
        context = {'data':advertisment,'jobs':jobs}
        return render(request,"advertisement_module/manage_jobSeeker.html",context)
    else:
        return HttpResponseNotFound("404")

def jobseeker_advertisement_detail(request,code):
    if check_verified_by_admin(request) and code:
        advertise = get_object_or_404(AdvertismentJobSeeker,advertise_code=code,jobSeeker = request.user.jobseeker)
        get_jobseeker = advertise.jobSeeker
        
        
        
        
        context = {'data':advertise,'province':get_jobseeker.province,'county':get_jobseeker.county,'district':get_jobseeker.district}
        return render(request,'advertisement_module/detail_jobseeker.html',context)
    return HttpResponseNotFound("404")


class JobSeekerCreateAdvertisement(View):
    def get(self,request,**kwargs):
        if check_jobSeeker(request):
            get_jobseeker = request.user.jobseeker
            get_advertisement = AdvertismentJobSeeker.objects.filter(jobSeeker = get_jobseeker)
            if get_advertisement.count()>1:
                return HttpResponse("شما نمیتوانید بیشتر از یک اگهی استخدام ایجاد کنید.")
            form =  JobSeekerAdvertisementModelForm()
            context = {'form':form}
            return render(request,"advertisement_module/jobseeker_create_advertisement.html",context)

    def post(self,request):
        if check_verified_by_admin(request):
            form = JobSeekerAdvertisementModelForm(request.POST)
            if form.is_valid():
                
                get_jobSeeker = request.user.jobseeker
                
                advertise = form.save(commit=False)
                
                advertise.province = get_jobSeeker.province
                
                advertise.county = get_jobSeeker.county
                
                if get_jobSeeker.district:
                    advertise.district = get_jobSeeker.district
                                
                advertise.jobSeeker = get_jobSeeker
                
                advertise.save()
                form.save_m2m()
                
                return redirect("jobseeker_manage")
            else:
                context ={'form':form}
                return render(request,"advertisement_module/jobseeker_create_advertisement.html",context)
        return HttpResponseNotFound("404")

class JobSeekerUpdateAdvertisementView(View):
    def get(self,request,**kwargs):
        if check_verified_by_admin(request):
            code = kwargs.get('code')
            if code:
                advertise = get_object_or_404(AdvertismentJobSeeker,advertise_code=code,jobSeeker=request.user.jobseeker)
                form = JobSeekerAdvertisementModelForm(instance=advertise)
                form.advertise_code = code
            
                context = {'form':form}
                return render(request,"advertisement_module/update_jobseeker_advertisement.html",context)
            else:
                return HttpResponseNotFound("404")
        else:
            return HttpResponseNotFound("404")
        
    def post(self,request,**kwargs):
        if check_verified_by_admin(request):

            code = kwargs.get('code')
            if code:
                advertise = get_object_or_404(AdvertismentJobSeeker,advertise_code=code)
                advertise_form_instance = get_object_or_404(AdvertismentJobSeeker,advertise_code=code)
                form = JobSeekerAdvertisementModelForm(request.POST,instance=advertise_form_instance)
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
                    form.save_m2m()
                    return redirect("jobseeker_manage")
                else:
                    context = {'form':form}
                    return render(request,"advertisement_module/update_jobseeker_advertisement.html",context)
            return HttpResponseNotFound("404")
        else:
            return HttpResponseNotFound("404")

def delete_jobseeker_advertisement(request,code):
    if check_verified_by_admin(request) and code:
        advertise = get_object_or_404(AdvertismentJobSeeker,advertise_code=code,jobSeeker = request.user.jobseeker)
        advertise.delete()
        
        return redirect('jobseeker_manage')
    return HttpResponseNotFound("404")

#endregion

# region history

def job_histories(request):
    if check_jobSeeker(request):
        jobSeeker = request.user.jobseeker
        jobs = jobSeeker.job_histories.all()
        
        context = {'jobs':jobs}
        return render(request,"advertisement_module/job_history_list.html",context)
    else:
        return HttpResponseNotFound("404")

class CreateJobHistory(View):
    def get(self,request):
        if check_jobSeeker:
            jobs = request.user.jobseeker.job_histories.all()
            if jobs.count() >=5:
                return HttpResponseNotFound("404")

            form = JobHistoryModelForm()
            context = {'form':form}
            return render(request,"advertisement_module/create_jobHistory.html",context)
        else:
            return HttpResponseNotFound("404")
        
    def post(self,request):
        if check_jobSeeker:
            form = JobHistoryModelForm(request.POST)
            if form.is_valid:
                history = form.save(commit=False)
                history.job_seeker = request.user.jobseeker
                history.save()
                return redirect("jobseeker_manage")
            else:
                context = {'form':form}
                return render(request,"advertisement_module/create_jobHistory.html",context)

class UpdateJobHistory(View):
    def get(self,request,**kwargs):
        if check_jobSeeker:
            code = kwargs.get('code')
            
            find_history = get_object_or_404(JobHistory,pk = code)
            
            form = JobHistoryModelForm(instance=find_history)
            context = {'form':form}
            return render(request,"advertisement_module/update_jobHistory.html",context)
        else:
            return HttpResponseNotFound("404")
        
    def post(self,request,**kwargs):
        if check_jobSeeker:
            code = kwargs.get('code')
            
            find_history = get_object_or_404(JobHistory,pk = code)

            
            form = JobHistoryModelForm(request.POST,instance=find_history)
            if form.is_valid():
                form.save()
                return redirect("jobseeker_manage")
            context = {'form':form}
            return render(request,"advertisement_module/update_jobHistory.html",context)
        else:
            return HttpResponseNotFound("404")

def delete_jobHistory(request,code):
    if check_jobSeeker:
        find_history = get_object_or_404(JobHistory,pk = code)
        find_history.delete()
        return redirect("jobseeker_manage")
    else:
        HttpResponseNotFound("404")
         
#endregion                

            
# region API


class SubscriptionModelViewSetApiView(ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionModelSerializer

class SkillModelViewSetApiView(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillModelSerializer

class DurationModelViewSetApiView(ModelViewSet):
    queryset = Duration.objects.all()
    serializer_class = DurationModelSerializer

class JobHistoryViewSetApiView(ModelViewSet):
    queryset = JobHistory.objects.all()
    serializer_class = JobHistoryModelSerializer

class AdvertismentModelViewSetApiView(ModelViewSet):
    queryset = Advertisment.objects.all().order_by('-created_at')
    serializer_class = AdvertisementModelSerializer
    
class AdvertismentJobSeekerModelViewSetApiView(ModelViewSet):
    queryset = AdvertismentJobSeeker.objects.all().order_by('-created_at')
    serializer_class = AdvertisementJobSeekerModelSerializer

#endregion

    
# ajax action
def get_cities(request:HttpRequest):
    province_id = int(request.GET.get('province_id'))
    try:
        cities = County.objects.filter(province_id=province_id).values("id", "name")
        return JsonResponse({"cities": list(cities)}, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)