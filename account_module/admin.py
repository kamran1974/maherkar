from django.contrib import admin
from .models import User,JobSeeker,Employer
from iranian_cities.models import Province , County
from iranian_cities.admin import IranianCitiesAdmin
# Register your models here.

class UserModelAdmin(admin.ModelAdmin):
    fields = [
        'user_type','first_name','last_name','email','phone','password','verify_code','is_staff',
        'is_superuser','is_active','groups','user_permissions'
    ]

class EmployerModelAdmin(admin.ModelAdmin):
    list_display =['persian_compnay_name','county','company_filed']
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset']= User.objects.filter(user_type = 'employer')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class JobSeekerModelAdmin(admin.ModelAdmin):
    autocomplete_fields = ['province', 'county']
    list_display = ['user','county','job_category']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset']= User.objects.filter(user_type = 'jobseeker')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    
admin.site.register(User,UserModelAdmin)
admin.site.register(Employer,EmployerModelAdmin)
admin.site.register(JobSeeker,JobSeekerModelAdmin)
