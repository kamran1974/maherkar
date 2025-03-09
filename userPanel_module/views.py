from django.http import HttpRequest,HttpResponseNotFound
from django.shortcuts import render,redirect
from django.views.generic.edit import UpdateView
from django import views
from account_module.models import User
from .forms import UpdateUserPsswordForm,UpdateUserForm,UpdateEmployerModelForm,UpdateJobSeekerModelForm
# Create your views here.

def user_dashboard(request:HttpRequest):
    if request.user.is_authenticated:
        get_user = request.user
        
        get_user_type = get_user.user_type
        
        user_type_info = None
        if get_user_type == 'employer':
            user_type_info = get_user.employer
            
        elif get_user_type == 'jobseeker':
            user_type_info = get_user.jobseeker
            
        else:
            return HttpResponseNotFound('404')
            
        context = {}
        if user_type_info:
            context = {'user':get_user , 'user_type':user_type_info}
        else:
            context = {'user':get_user}
        
        return render(request,'userPanel_module/index.html',context)
            
    return redirect("login")

class UpdateUserView(views.View):
    def get(self,request):
        if request.user.is_authenticated:
            get_user = request.user
            form = UpdateUserForm(instance=get_user)
            context = {'form':form}
            return render(request,"userPanel_module/update_user.html",context)
        return redirect("login")
    def post(self,request):
        if request.user.is_authenticated:
            get_user = request.user
            form = UpdateUserForm(request.POST,instance = get_user)
            if form.is_valid():
                form.save()
                return redirect("user_dashboard")
            else:    
                context = {'form':form}
                return render(request,"userPanel_module/update_user.html",context)
        return redirect("login")
           
class UpdateUserPasswordView(views.View):
    def get(self,request:HttpRequest):
        if request.user.is_authenticated:
            form = UpdateUserPsswordForm()
            context = {'form':form}
            return render(request,"userPanel_module/update_password.html",context)
        return redirect("login")
    
    def post(self,request):
        if request.user.is_authenticated:
            get_user = request.user
            
            form = UpdateUserPsswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data.get('password')
                User.set_password(get_user,new_password)
                get_user.save()
                return redirect('login')
            else:
                context = {'form':form}
                return render(request,"userPanel_module/update_password.html",context)
        else:
            return redirect('login')

class UpdateEmployerView(views.View):
    def get(self,request):
        if request.user.is_authenticated:
            get_user = request.user
            if get_user.user_type =="employer":
                get_user = get_user.employer
                form = UpdateEmployerModelForm(instance=get_user)
                context = {'form':form}
                return render(request,"userPanel_module/update_employer.html",context)
            else:
                return HttpResponseNotFound("404")
        return redirect("login")
    def post(self,request):
        if request.user.is_authenticated:
            get_user = request.user
            if get_user.user_type =="employer":
                get_user = get_user.employer
                form = UpdateEmployerModelForm(request.POST,instance=get_user)
                if form.is_valid():
                    form.save()
                    get_user.verified_by_admin = False
                    get_user.save()
                    return redirect("user_dashboard")
                else:

                    context = {'form':form}
                    return render(request,"userPanel_module/update_employer.html",context)
            else:
                return HttpResponseNotFound("404")
        return redirect("login")
        
class UpdateJobSeekerView(views.View):
    def get(self,request):
        if request.user.is_authenticated:
            get_user = request.user
            if get_user.user_type =="jobseeker":
                get_user = get_user.jobseeker
                form = UpdateJobSeekerModelForm(instance=get_user)
                context = {'form':form}
                return render(request,"userPanel_module/update_jobseeker.html",context)
            else:
                return HttpResponseNotFound("404")
        return redirect("login")
    def post(self,request):
        if request.user.is_authenticated:
            get_user = request.user
            if get_user.user_type =="jobseeker":
                get_user = get_user.jobseeker
                form = UpdateJobSeekerModelForm(request.POST,instance=get_user)
                if form.is_valid():
                    form.save()
                    return redirect("user_dashboard")
                else:

                    context = {'form':form}
                    return render(request,"userPanel_module/update_jobseeker.html",context)
            else:
                return HttpResponseNotFound("404")
        return redirect("login")
                
                

