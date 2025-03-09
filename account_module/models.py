from django.contrib.auth.models import AbstractUser
from django.db import models
from iranian_cities.fields import ProvinceField, CountyField
from django.utils.crypto import get_random_string
from home_module.models import TehranDistrict
from jobAndCompanyActivity_module.models import Job, CompanyActivity
from random import randrange
from datetime import datetime, timedelta

class User(AbstractUser):
    """مدل کاربر با فیلدهای سفارشی."""
    
    USER_TYPES = (('admin', 'ادمین'), ("employer", "کارفرما"), ('jobseeker', 'کارجو'))
    
    user_type = models.CharField(max_length=120, choices=USER_TYPES, verbose_name="نوع کاربر")
    first_name = models.CharField(max_length=150, verbose_name="نام")
    last_name = models.CharField(max_length=150, verbose_name="نام خانوادگی")
    email = models.EmailField(unique=True, verbose_name="ایمیل", db_index=True)
    phone = models.CharField(max_length=120, verbose_name='شماره تلفن')
    password = models.CharField(max_length=220, verbose_name="رمز عبور")
    verify_code = models.CharField(max_length=120, null=True, blank=True, verbose_name='کد تایید')
    expire_date_code = models.DateTimeField(verbose_name='تاریخ انقضا کد', blank=True, null=True)
    
    def new_verify_code(self):
        """تولید کد تایید جدید و تعیین تاریخ انقضا."""
        self.verify_code = randrange(100000, 999999)
        now = datetime.now()
        self.expire_date_code = now + timedelta(minutes=2)
        self.save()
    
    def __str__(self):
        """نمایش نام و نوع کاربر."""
        display_type = ''
        if self.user_type == 'admin':
            display_type = 'ادمین'
        elif self.user_type == 'employer':
            display_type = 'کارفرما'
        else:
            display_type = 'کارجو'
        return f"{self.first_name} {self.last_name} ({display_type})"


class Employer(models.Model):
    """مدل کارفرما با اطلاعات شرکت."""
    
    PERSON_COUNTER = (
        ('1', "یک نفر"), ('2-10', "2 تا 10 نفر"), ('11-50', "11 تا 50 نفر"),
        ('51-200', "51 تا 200 نفر"), ('201-500', "201 تا 500 نفر"),
        ('501-1000', "501 تا 1000 نفر"), ('1000+', "بیش از 1000 نفر")
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر', related_name='employer')
    persian_company_name = models.CharField(max_length=220, verbose_name="نام شرکت به فارسی")
    description = models.TextField(verbose_name="اطلاعاتی درمورد شرکت", null=True, blank=True)
    company_name = models.CharField(max_length=220, verbose_name="نام شرکت به انگلیسی")
    company_logo = models.ImageField(verbose_name='لوگو شرکت', null=True, blank=True, upload_to='images/company_logo')
    site_address = models.URLField(verbose_name='آدرس سایت شرکت', blank=True, null=True)
    company_field = models.ForeignKey(CompanyActivity, verbose_name='حوزه فعالیت شرکت', on_delete=models.CASCADE)
    person_count = models.CharField(max_length=120, choices=PERSON_COUNTER, verbose_name='تعداد پرسنل')
    verified_by_admin = models.BooleanField(verbose_name="تایید شده توسط ادمین", default=False)
    province = ProvinceField(verbose_name='نام استان')
    county = CountyField(verbose_name="نام شهرستان")
    district = models.ForeignKey(TehranDistrict, on_delete=models.CASCADE, verbose_name='نام منطقه', null=True, blank=True)

    def __str__(self):
        """نمایش نوع کاربر و نام شرکت."""
        return f"{self.user.user_type} {self.company_name}"
    
    class Meta:
        verbose_name = 'کارفرما'
        verbose_name_plural = 'کارفرمایان'


class JobSeeker(models.Model):
    """مدل کارجو با اطلاعات شغلی و مکانی."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر', related_name='jobseeker')
    job_category = models.ForeignKey(Job, verbose_name="شغل", on_delete=models.CASCADE)
    province = ProvinceField(verbose_name='نام استان')
    county = CountyField(verbose_name="نام شهرستان")
    district = models.ForeignKey(TehranDistrict, on_delete=models.CASCADE, verbose_name='نام منطقه', null=True, blank=True)
    
    class Meta:
        verbose_name = 'کارجو'
        verbose_name_plural = 'کارجویان'
        
    def __str__(self):
        """نمایش نام کارجو، شغل و شهرستان."""
        return f"{self.user.first_name} {self.user.last_name} - {self.job_category} , {self.county}"
