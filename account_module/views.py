from django.contrib.auth import login, logout
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import (HttpRequest, HttpResponse, HttpResponseNotFound,
                         JsonResponse)
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from iranian_cities.models import County, Province

from advertisement_module.models import Advertisment

from .serializers import EmployerSerializer, JobSeekerSerializer, UserSerializer
from utils.emailService import send_email
from utils.smsService import send_sms

from .forms import (ChangePasswordForm, EmployerRegisterModelForm,
                    ForgotPasswordForm, JobSeekerRegisterForm, LoginForm,
                    RegisterForm,ActiveAccountForm)
from .models import Employer, JobSeeker, User
from rest_framework.viewsets import ModelViewSet
from datetime import datetime
from random import randrange



class RegisterView(View):
    def get(self,request):
        form = RegisterForm()
        context = {'form' : form}
        return render(request,'account_module/register.html',context)
    
    def post(self,request):
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            
            get_email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')

            email_exist = User.objects.filter(email__iexact=get_email).exists()
            phone_exist = User.objects.filter(phone = phone).exists()

            if email_exist:
                form.add_error('email', "ایمیل وارد شده تکراری است.")
            elif phone_exist:
                form.add_error('phone', "شماره تلفن  وارد شده تکراری است.")
            else:    
            
                email = form.cleaned_data.get("email")
                password = form.cleaned_data.get("password")
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                user_type = form.cleaned_data.get('user_type')
                
                user_name = str(email).split('@')[0]
                
                new_user = User(username=user_name,first_name = first_name , last_name = last_name ,email = email,phone=phone,user_type=user_type,is_active=False)

            
                new_user.set_password(password)
                        
                new_user.new_verify_code()
                new_user.save()
                # send_email('email/active_account.html',new_user.email,{"verify_code" :new_user.verify_code},"فعالسازی حساب")
                # send_sms(new_user.phone,new_user.verify_code,"verifyaccount")
                request.session['phone'] = new_user.phone
                
                
                if new_user.user_type == "employer":
                    return redirect('register_employer')
                elif new_user.user_type == 'jobseeker':
                    return redirect('register_jobseeker')    
                

        context = {'form': form}
        return render(request, 'account_module/register.html', context)
        

class RegisterEmployer(View):
    def get(self,request):
        phone = request.session.get('phone')
        
        if phone:
            find_user = get_object_or_404(User,phone=phone)
            
            if find_user.user_type == "employer":
                form = EmployerRegisterModelForm()
                context = {'form':form}
                return render(request,"account_module/register_employer.html",context)
            else:
                return HttpResponseNotFound()
        else:
            return HttpResponseNotFound()
        
    def post(self,request,**kwargs):
        phone = request.session.get('phone')
        
        if phone:
            find_user = get_object_or_404(User,phone=phone)
            
            if find_user.user_type == "employer":
                form = EmployerRegisterModelForm(request.POST,request.FILES)
                
                if form.is_valid():
                    
                    new_employer = form.save(commit=False)
                    
                    new_employer.user = find_user
                    
                    new_employer.save()
                    
                    # find_user.new_verify_code()
                    del request.session['phone']
                    return redirect('login')
                else:
                    context = {'form':form}
                    return render(request,"account_module/register_employer.html",context)
            else:
                return HttpResponseNotFound()
        else:
            return HttpResponseNotFound()
        
        
class RegisterJobSeeker(View):
    def get(self,request,**kwargs):
        phone = request.session.get('phone')
        
        if phone:
            find_user = get_object_or_404(User,phone=phone)
            
            if find_user.user_type == "jobseeker":
                form = JobSeekerRegisterForm()
                context = {'form':form}
                return render(request,"account_module/register_jobseeker.html",context)
            else:
                return HttpResponseNotFound()
        else:
            return HttpResponseNotFound()
        
        
    
    def post(self,request,**kwargs):
        phone = request.session.get('phone')
        
        if phone:
            find_user = get_object_or_404(User,phone=phone)
            
            if find_user.user_type == "jobseeker":
                form = JobSeekerRegisterForm(request.POST,request.FILES)
                
                if form.is_valid():
                    
                    new_jobseeker = form.save(commit=False)
                    
                    new_jobseeker.user = find_user
                    
                    new_jobseeker.save()
                    
                    # find_user.new_verify_code()
                    
                    del request.session['phone']
                    
                    return redirect('login')
                else:
                    form = JobSeekerRegisterForm()
                    context = {'form':form}
                    return render(request,"account_module/register_jobseeker.html",context)
            else:
                return HttpResponseNotFound()
        else:
            return HttpResponseNotFound()
        
# ajax action
def get_cities(request:HttpRequest):
    province_id = int(request.GET.get('province_id'))
    try:
        cities = County.objects.filter(province_id=province_id).values("id", "name")
        return JsonResponse({"cities": list(cities)}, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
    
class ActiveAccountView(View):
    def get(self,request):
        if request.session.get("phone") == "" or None:
            return HttpResponseNotFound(404)
        
        phone = request.session.get("phone")    
        user = get_object_or_404(User,phone = phone)
        form = ActiveAccountForm()
        expire_date = user.expire_date_code.isoformat()
        context = {'form':form,'phone':phone ,"expire_time":expire_date}
        return render(request,"account_module/active_account2.html",context)
    
    def post(self,request):
        
        if request.session.get("phone") == "" or None:
            return HttpResponseNotFound(404)
        
        phone = request.session.get("phone")    
        find_user = get_object_or_404(User,phone = phone)
        form = ActiveAccountForm(request.POST)
        if form.is_valid():
            active_code = form.cleaned_data.get('code')
            if find_user.verify_code == active_code:
                now = datetime.now()
                if find_user.expire_date_code >now:
                    get_type = find_user.user_type
                    
                    if get_type == 'employer':
                        check_register = Employer.objects.filter(user = find_user).exists()
                        if check_register == False:
                            
                            find_user.new_verify_code()
                            
                            return redirect('register_employer',verify_code=find_user.verify_code)
                    elif get_type == 'jobseeker':
                            check_register = JobSeeker.objects.filter(user = find_user).exists()
                            if check_register == False:
                            
                                find_user.new_verify_code()
                            
                                return redirect('register_jobseeker',verify_code=find_user.verify_code)
                            
                    find_user.is_active = True
                    find_user.new_verify_code()
                    login(request,find_user)
                    return redirect('user_dashboard')
 
                    
                else:
                    form.add_error('code',"کد مننضی شده است")
            else:
                form.add_error('code',"کد اشتباه است")
        
        context = {'form':form,'phone':request.session.get('phone')}
        return render(request,"account_module/active_account.html",context)
        

class ForgotPassword(View):
    def get(self,request):
        form = ForgotPasswordForm()
        context = {'form':form}
        return render(request,"account_module/forgot_password.html",context)
    
    def post(self,request):
        form = ForgotPasswordForm(request.POST)
        
        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            find_user = get_object_or_404(User,phone=phone)
            new_password = str(randrange(100000,999999))
            find_user.set_password(new_password)
            find_user.save()
            send_sms(find_user.phone,new_password,'forgot-password')
            return redirect('login')
        else:
            return HttpResponseNotFound()
            
            # 

class ChangePassword(View):
    def get(self,request,**kwargs):
        code = kwargs['verify_code']
            
        get_object_or_404(User,verify_code=code)
        form = ChangePasswordForm()
        context = {"form":form}
        return render(request,"account_module/change_password.html",context)
    
    def post(self,request,**kwargs):
        form = ChangePasswordForm(request.POST)
        
        if form.is_valid():
            code = kwargs['verify_code']
            
            find_user = get_object_or_404(User,verify_code=code)
            
            new_password = form.cleaned_data.get('password')
            
            find_user.set_password(new_password)
            
            find_user.is_active=True
            
            find_user.new_verify_code()
            
            find_user.save()
            
            return redirect('login')
        else:
            context = {"form":form}
            return render(request,"account_module/change_password.html",context)
            
class Login(View):
    def get(self,request):
        form = LoginForm()
        context = {"form":form}
        return render(request,"account_module/login.html",context)
    
    def post(self,request):
        form = LoginForm(request.POST)
        
        if form.is_valid():
            phone = form.cleaned_data.get('phone')            
            try:
                find_user = User.objects.get(phone = phone)
            except:
                find_user = None
            
            if find_user == None:
                form.add_error('phone','حساب یافت نشد')
            else:
                    get_type = find_user.user_type
                    
                    if get_type == 'employer':
                        check_register = Employer.objects.filter(user = find_user).exists()
                        if check_register == False:
                            
                            find_user.new_verify_code()
                            
                            return redirect('register_employer')
                    elif get_type == 'jobseeker':
                            check_register = JobSeeker.objects.filter(user = find_user).exists()
                            if check_register == False:
                            
                                find_user.new_verify_code()
                            
                                return redirect('register_jobseeker')

                    find_user.new_verify_code()
                    request.session['phone'] = find_user.phone
                    send_sms(find_user.phone,find_user.verify_code,'verifyaccount')
                    return redirect('active_account')
                    # login(request,find_user)
                        # if get_type == "employer":
                        #     return redirect('dashboard')
                    # return pass
        context = {'form':form}
        return render(request,"account_module/login.html",context)
                    
def logout_view(request:HttpRequest):
    if request.user.is_authenticated:
        logout(request) 
    return redirect('login')


# ajax action
def reSend_activeCode(request):
    phone = request.GET.get('phone')
    find_user = get_object_or_404(User,phone = phone)
    find_user.new_verify_code()
    send_sms(find_user.phone,find_user.verify_code,"verifyaccount")
    return JsonResponse({"status":200})

        
# API

class UserViewSetApiView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class EmployerViewSetApiView(ModelViewSet):
        queryset = Employer.objects.all()
        serializer_class = EmployerSerializer
        
class JobSeekerViewSetApiView(ModelViewSet):
    queryset = JobSeeker.objects.all()
    serializer_class = JobSeekerSerializer