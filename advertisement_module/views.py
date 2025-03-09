# ایمپورت‌های مورد نیاز
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from rest_framework.viewsets import ModelViewSet
from iranian_cities.models import County

from account_module.models import Employer
from advertisement_module.models import (
    Advertisement,
    AdvertisementJobSeeker,
    AdDisplayDuration,
    JobHistory,
    ReportAdvertisment,
    Subscription,
    Skill
)
from advertisement_module.serializers import (
    AdvertisementModelSerializer,
    AdvertisementJobSeekerModelSerializer,
    AdDisplayDurationModelSerializer,
    JobHistoryModelSerializer,
    SubscriptionModelSerializer,
    SkillModelSerializer
)
from advertisement_module.forms import (
    AdvertisementModelForm,
    JobHistoryModelForm,
    JobSeekerAdvertisementModelForm,
    ReportAdvertisment,
    UpdateAdvertisementModelForm
)


# فانکشن‌های ابزار برای بررسی نوع کاربر و وضعیت تایید توسط ادمین
def check_employer(request: HttpRequest) -> bool:
    """بررسی اینکه آیا کاربر فعلی یک کارفرما است."""
    if request.user.is_authenticated:
        return request.user.user_type == "employer"
    return False


def check_job_seeker(request: HttpRequest) -> bool:
    """بررسی اینکه آیا کاربر فعلی یک جویای کار است."""
    if request.user.is_authenticated:
        return request.user.user_type == "jobseeker"
    return False


def check_verified_by_admin(request: HttpRequest) -> bool:
    """بررسی اینکه آیا کاربر (کارفرما) توسط ادمین تایید شده است یا خیر."""
    if request.user.is_authenticated:
        if request.user.user_type == "employer":
            return request.user.employer.verified_by_admin
        elif request.user.user_type == "jobseeker":
            return True
    return False


# ویوها
def dashboard(request: HttpRequest) -> HttpResponse:
    """نمایش داشبورد کارفرما."""
    if check_employer(request):
        get_user_name = request.user.first_name
        check_verified_by_admin_status = request.user.employer.verified_by_admin
        
        context = {'name': get_user_name, 'status': check_verified_by_admin_status}
        return render(request, 'advertisement_module/home.html', context)
    return HttpResponseNotFound("404")


def advertisement_list(request: HttpRequest) -> HttpResponse:
    """لیست آگهی‌های مربوط به کارفرما."""
    if check_verified_by_admin(request):
        get_employer = request.user.employer
        advertisements = Advertisement.objects.filter(employer=get_employer).order_by('created_at')
        
        context = {'advertisements': advertisements}
        return render(request, "advertisement_module/manage.html", context)
    return HttpResponseNotFound("404")


def advertisement_detail(request: HttpRequest, code: str) -> HttpResponse:
    """نمایش جزئیات یک آگهی خاص."""
    if check_verified_by_admin(request) and code:
        advertisement = get_object_or_404(Advertisement, advertise_code=code)
        get_employer = advertisement.employer
        
        context = {'data': advertisement, 'province': get_employer.province, 'county': get_employer.county, 'district': get_employer.district}
        return render(request, 'advertisement_module/detail.html', context)
    return HttpResponseNotFound("404")


class CreateAdvertisement(View):
    """ویو کلاس‌بنیاد برای ایجاد آگهی جدید."""
    def get(self, request: HttpRequest) -> HttpResponse:
        if check_verified_by_admin(request):
            form = AdvertisementModelForm()
            context = {'form': form}
            return render(request, "advertisement_module/create.html", context)
        return HttpResponseNotFound("404")

    def post(self, request: HttpRequest) -> HttpResponse:
        if check_verified_by_admin(request):
            form = AdvertisementModelForm(request.POST)
            if form.is_valid():
                get_employer = request.user.employer
                advertisement = form.save(commit=False)
                
                advertisement.province = get_employer.province
                advertisement.county = get_employer.county
                
                if get_employer.district:
                    advertisement.district = get_employer.district
                
                advertisement.employer = get_employer
                advertisement.save()
                form.save_m2m()
                
                return redirect("dashboard")
            else:
                context = {'form': form}
                return render(request, "advertisement_module/create.html", context)
        return HttpResponseNotFound("404")


class UpdateAdvertisementView(View):
    """ویو کلاس‌بنیاد برای بروزرسانی یک آگهی."""
    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        if check_verified_by_admin(request):
            code = kwargs.get('code')
            if code:
                advertisement = get_object_or_404(Advertisement, advertise_code=code)
                form = UpdateAdvertisementModelForm(instance=advertisement)
            
                context = {'form': form}
                return render(request, "advertisement_module/update.html", context)
        return HttpResponseNotFound("404")
        
    def post(self, request: HttpRequest, **kwargs) -> HttpResponse:
        if check_verified_by_admin(request):
            code = kwargs.get('code')
            if code:
                advertisement_instance = get_object_or_404(Advertisement, advertise_code=code)
                form = UpdateAdvertisementModelForm(request.POST, instance=advertisement_instance)
                
                if form.is_valid():
                    advertisement_form = form.save(commit=False)
                    advertisement_form.advertise_code = code
                    advertisement_form.is_show = False
                    advertisement_form.check_by_admin = False
                    advertisement_form.status = 'pending'
                    
                    if advertisement_form.duration_id != advertisement_instance.duration_id or advertisement_form.subscription_id != advertisement_instance.subscription_id:
                        duration_price = 0
                        subscription_price = 0
                        
                        if advertisement_form.duration_id != advertisement_instance.duration_id:
                            duration_price = AdDisplayDuration.objects.get(pk=advertisement_form.duration_id).price
                        if advertisement_form.subscription_id != advertisement_instance.subscription_id:
                            subscription_price = Subscription.objects.get(pk=advertisement_form.subscription_id).price
                        
                        total_price = duration_price + subscription_price
                        advertisement_form.total_price = total_price
                        
                        if advertisement_form.total_price > 0:
                            advertisement_form.pay_status = False
                            advertisement_form.status = "unpaid"
                
                    advertisement_form.save()
                    form.save_m2m()
                    return redirect("advertisement_manage")
                else:
                    context = {'form': form}
                    return render(request, "advertisement_module/update.html", context)
            return HttpResponseNotFound("404")
        return HttpResponseNotFound("404")


def delete_advertisement(request: HttpRequest, code: str) -> HttpResponse:
    """حذف یک آگهی خاص."""
    if check_verified_by_admin(request) and code:
        advertisement = get_object_or_404(Advertisement, advertise_code=code)
        advertisement.delete()
        
        return redirect('advertisement_manage')
    return HttpResponseNotFound("404")


def job_seeker_advertisement_list(request: HttpRequest) -> HttpResponse:
    """نمایش لیست آگهی‌های جویای کار."""
    if check_job_seeker(request):
        try:
            advertisement = AdvertisementJobSeeker.objects.get(jobSeeker=request.user.jobseeker)
        except AdvertisementJobSeeker.DoesNotExist:
            advertisement = None
        
        jobs = request.user.jobseeker.job_histories.all()
        
        context = {'data': advertisement, 'jobs': jobs}
        return render(request, "advertisement_module/manage_jobSeeker.html", context)
    return HttpResponseNotFound("404")


def job_seeker_advertisement_detail(request: HttpRequest, code: str) -> HttpResponse:
    """نمایش جزئیات یک آگهی خاص برای جویای کار."""
    if check_verified_by_admin(request) and code:
        advertisement = get_object_or_404(AdvertisementJobSeeker, advertise_code=code, jobSeeker=request.user.jobseeker)
        job_seeker = advertisement.jobSeeker
        
        context = {'data': advertisement, 'province': job_seeker.province, 'county': job_seeker.county, 'district': job_seeker.district}
        return render(request, 'advertisement_module/detail_jobseeker.html', context)
    return HttpResponseNotFound("404")


class JobSeekerCreateAdvertisement(View):
    """ویو کلاس‌بنیاد برای ایجاد آگهی جدید توسط جویای کار."""
    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        if check_job_seeker(request):
            job_seeker = request.user.jobseeker
            existing_advertisements = AdvertisementJobSeeker.objects.filter(jobSeeker=job_seeker)
            
            if existing_advertisements.count() > 1:
                return HttpResponse("شما نمی‌توانید بیشتر از یک آگهی استخدام ایجاد کنید.")
            
            form = JobSeekerAdvertisementModelForm()
            context = {'form': form}
            return render(request, "advertisement_module/jobseeker_create_advertisement.html", context)
        return HttpResponseNotFound("404")

    def post(self, request: HttpRequest) -> HttpResponse:
        if check_verified_by_admin(request):
            form = JobSeekerAdvertisementModelForm(request.POST)
            if form.is_valid():
                job_seeker = request.user.jobseeker
                advertisement = form.save(commit=False)
                
                advertisement.province = job_seeker.province
                advertisement.county = job_seeker.county
                
                if job_seeker.district:
                    advertisement.district = job_seeker.district
                
                advertisement.jobSeeker = job_seeker
                advertisement.save()
                form.save_m2m()
                
                return redirect("jobseeker_manage")
            else:
                context = {'form': form}
                return render(request, "advertisement_module/jobseeker_create_advertisement.html", context)
        return HttpResponseNotFound("404")


class JobSeekerUpdateAdvertisementView(View):
    """ویو کلاس‌بنیاد برای بروزرسانی آگهی جویای کار."""
    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        if check_verified_by_admin(request):
            code = kwargs.get('code')
            if code:
                advertisement = get_object_or_404(AdvertisementJobSeeker, advertise_code=code, jobSeeker=request.user.jobseeker)
                form = JobSeekerAdvertisementModelForm(instance=advertisement)
            
                context = {'form': form}
                return render(request, "advertisement_module/update_jobseeker_advertisement.html", context)
        return HttpResponseNotFound("404")
        
    def post(self, request: HttpRequest, **kwargs) -> HttpResponse:
        if check_verified_by_admin(request):
            code = kwargs.get('code')
            if code:
                advertisement_instance = get_object_or_404(AdvertisementJobSeeker, advertise_code=code)
                form = JobSeekerAdvertisementModelForm(request.POST, instance=advertisement_instance)
                
                if form.is_valid():
                    advertisement_form = form.save(commit=False)
                    advertisement_form.advertise_code = code
                    advertisement_form.is_show = False
                    advertisement_form.check_by_admin = False
                    advertisement_form.status = 'pending'
                    
                    if advertisement_form.duration_id != advertisement_instance.duration_id or advertisement_form.subscription_id != advertisement_instance.subscription_id:
                        duration_price = 0
                        subscription_price = 0
                        
                        if advertisement_form.duration_id != advertisement_instance.duration_id:
                            duration_price = AdDisplayDuration.objects.get(pk=advertisement_form.duration_id).price
                        if advertisement_form.subscription_id != advertisement_instance.subscription_id:
                            subscription_price = Subscription.objects.get(pk=advertisement_form.subscription_id).price
                        
                        total_price = duration_price + subscription_price
                        advertisement_form.total_price = total_price
                        
                        if advertisement_form.total_price > 0:
                            advertisement_form.pay_status = False
                            advertisement_form.status = "unpaid"
                
                    advertisement_form.save()
                    form.save_m2m()
                    return redirect("jobseeker_manage")
                else:
                    context = {'form': form}
                    return render(request, "advertisement_module/update_jobseeker_advertisement.html", context)
            return HttpResponseNotFound("404")
        return HttpResponseNotFound("404")


def delete_job_seeker_advertisement(request: HttpRequest, code: str) -> HttpResponse:
    """حذف یک آگهی خاص توسط جویای کار."""
    if check_verified_by_admin(request) and code:
        advertisement = get_object_or_404(AdvertisementJobSeeker, advertise_code=code, jobSeeker=request.user.jobseeker)
        advertisement.delete()
        
        return redirect('jobseeker_manage')
    return HttpResponseNotFound("404")


def job_histories(request: HttpRequest) -> HttpResponse:
    """نمایش لیست تاریخچه‌های شغلی مربوط به جویای کار."""
    if check_job_seeker(request):
        job_seeker = request.user.jobseeker
        jobs = job_seeker.job_histories.all()
        
        context = {'jobs': jobs}
        return render(request, "advertisement_module/job_history_list.html", context)
    return HttpResponseNotFound("404")


class CreateJobHistory(View):
    """ویو کلاس‌بنیاد برای ایجاد تاریخچه شغلی جدید."""
    def get(self, request: HttpRequest) -> HttpResponse:
        if check_job_seeker(request):
            jobs = request.user.jobseeker.job_histories.all()
            if jobs.count() >= 5:
                return HttpResponseNotFound("404")

            form = JobHistoryModelForm()
            context = {'form': form}
            return render(request, "advertisement_module/create_jobHistory.html", context)
        return HttpResponseNotFound("404")
        
    def post(self, request: HttpRequest) -> HttpResponse:
        if check_job_seeker(request):
            form = JobHistoryModelForm(request.POST)
            if form.is_valid():
                history = form.save(commit=False)
                history.job_seeker = request.user.jobseeker
                history.save()
                return redirect("jobseeker_manage")
            else:
                context = {'form': form}
                return render(request, "advertisement_module/create_jobHistory.html", context)
        return HttpResponseNotFound("404")


class UpdateJobHistory(View):
    """ویو کلاس‌بنیاد برای بروزرسانی تاریخچه شغلی."""
    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        if check_job_seeker(request):
            code = kwargs.get('code')
            find_history = get_object_or_404(JobHistory, pk=code)
            
            form = JobHistoryModelForm(instance=find_history)
            context = {'form': form}
            return render(request, "advertisement_module/update_jobHistory.html", context)
        return HttpResponseNotFound("404")
        
    def post(self, request: HttpRequest, **kwargs) -> HttpResponse:
        if check_job_seeker(request):
            code = kwargs.get('code')
            find_history = get_object_or_404(JobHistory, pk=code)
            
            form = JobHistoryModelForm(request.POST, instance=find_history)
            if form.is_valid():
                form.save()
                return redirect("jobseeker_manage")
            context = {'form': form}
            return render(request, "advertisement_module/update_jobHistory.html", context)
        return HttpResponseNotFound("404")


def delete_job_history(request: HttpRequest, code: str) -> HttpResponse:
    """حذف یک تاریخچه شغلی خاص توسط جویای کار."""
    if check_job_seeker(request):
        find_history = get_object_or_404(JobHistory, pk=code)
        find_history.delete()
        return redirect('jobseeker_manage')
    return HttpResponseNotFound("404")


# ویوست‌های API برای مدل‌های مختلف با استفاده از DRF (Django Rest Framework)
class SubscriptionModelViewSetApiView(ModelViewSet):
    """ViewSet برای مدیریت API مربوط به Subscription."""
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionModelSerializer


class SkillModelViewSetApiView(ModelViewSet):
    """ViewSet برای مدیریت API مربوط به Skill."""
    queryset = Skill.objects.all()
    serializer_class = SkillModelSerializer


class AdDisplayDurationModelViewSetApiView(ModelViewSet):
    """ViewSet برای مدیریت API مربوط به AdDisplayDuration."""
    queryset = AdDisplayDuration.objects.all()
    serializer_class = AdDisplayDurationModelSerializer


class JobHistoryViewSetApiView(ModelViewSet):
    """ViewSet برای مدیریت API مربوط به JobHistory."""
    queryset = JobHistory.objects.all()
    serializer_class = JobHistoryModelSerializer


class AdvertisementModelViewSetApiView(ModelViewSet):
    """ViewSet برای مدیریت API مربوط به Advertisement."""
    queryset = Advertisement.objects.all().order_by('-created_at')
    serializer_class = AdvertisementModelSerializer


class AdvertisementJobSeekerModelViewSetApiView(ModelViewSet):
    """ViewSet برای مدیریت API مربوط به AdvertisementJobSeeker."""
    queryset = AdvertisementJobSeeker.objects.all().order_by('-created_at')
    serializer_class = AdvertisementJobSeekerModelSerializer


# فانکشن برای مدیریت درخواست‌های Ajax به منظور دریافت شهرها
def get_cities(request: HttpRequest) -> JsonResponse:
    """
    دریافت لیست شهرها بر اساس شناسه استان (province_id) از طریق درخواست Ajax.
    """
    province_id = int(request.GET.get('province_id'))
    try:
        cities = County.objects.filter(province_id=province_id).values("id", "name")
        return JsonResponse({"cities": list(cities)}, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
