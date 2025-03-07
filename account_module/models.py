from django.contrib.auth.models import AbstractUser
from django.db import models
from iranian_cities.fields import ProvinceField , CountyField
from django.utils.crypto import get_random_string
from home_module.models import TehranDistrict
from jobAndCompanyActivity_module.models import Job,CompanyActivity
from random import randrange
from datetime import datetime,timedelta

class User(AbstractUser):
    
    USER_TYPES = (('admin','ادمین'),("employer","کارفرما"),('jobseeker','کارجو'))

    user_type = models.CharField(max_length=120, choices=USER_TYPES,verbose_name="نوع کاربر")

    first_name = models.CharField(max_length=150,verbose_name="نام")

    last_name = models.CharField(max_length=150,verbose_name="نام خانوادگی")

    email = models.EmailField(unique=True,verbose_name="ایمیل",db_index=True)
    
    phone = models.CharField(max_length=120,verbose_name='شماره تلفن')

    password = models.CharField(max_length=220,verbose_name="رمز عبور")
    
    verify_code = models.CharField(max_length=120,null=True,blank=True,verbose_name='کد تایید')
    
    expire_date_code = models.DateTimeField(verbose_name='تاریخ انقضا کد',blank=True,null=True)
    
    
    def new_verify_code(self):
        self.verify_code = randrange(100000,999999)
        now = datetime.now()
        expire = now + timedelta(minutes=2)
        self.expire_date_code = expire
        self.save()
    

    def __str__(self):
        display_type = ''
        city = ""
        if self.user_type == 'admin':
            display_type = 'ادمین'
        elif self.user_type == 'employer':
            display_type = 'کارفرما'
        else:
            display_type = 'کارجو'
            
        return f"{self.first_name} {self.last_name} ({display_type})"

class Employer(models.Model):

    # COMPANY_FIELDS = (('بیمه','بیمه'),('نفت و گاز','نفت و گاز'),('کامپیوتر، فناوری اطلاعات و اینترنت','کامپیوتر، فناوری اطلاعات و اینترنت'),('نیرو','نیرو'),('منابع انسانی','منابع انسانی'),('رسانه و انتشارات','رسانه و انتشارات'),('تبلیغات، بازاریابی و برندسازی','تبلیغات، بازاریابی و برندسازی'),('مخابرات و ارتباطات (تلکام)','مخابرات و ارتباطات (تلکام)'),('آموزش، مدارس و دانشگاه‌ها','آموزش، مدارس و دانشگاه‌ها'),('معماری و عمران','معماری و عمران'),('تولید و صنایع','تولید و صنایع'),('املاک و مستغلات','املاک و مستغلات'),('دولتی','دولتی'),('مالی و اعتباری','مالی و اعتباری'),('خدمات درمانی، پزشکی و سلامت','خدمات درمانی، پزشکی و سلامت'),('گردشگری و هتل‌ها','گردشگری و هتل‌ها'),('وکالت و حقوقی','وکالت و حقوقی'),('استاندارد و کنترل‌کیفیت','استاندارد و کنترل‌کیفیت'),('بانکداری','بانکداری'),('حمل و نقل، لاجستیک و انبارداری','حمل و نقل، لاجستیک و انبارداری'),('خرده‌فروشی، عمده‌فروشی و فروشگاه‌های زنجیره‌ای','خرده‌فروشی، عمده‌فروشی و فروشگاه‌های زنجیره‌ای'),('خودروسازی','خودروسازی'),('سازمان‌های مردم‌نهاد (NGO)','سازمان‌های مردم‌نهاد (NGO)'),('سرمایه‌گذاری و تحلیل کسب‌وکار','سرمایه‌گذاری و تحلیل کسب‌وکار'),('غذا و رستوران‌ها','غذا و رستوران‌ها'),('فرهنگی و ورزشی','فرهنگی و ورزشی'),('کالای مصرفی و خوراکی','کالای مصرفی و خوراکی'),('کشاورزی','کشاورزی'),('واردات و صادرات','واردات و صادرات'))
    
    PERSON_COUNTER = (('1',"یک نفر"),('2-10',"2 تا 10 نفر"),('11-50',"11 تا 50 نفر"),('51-200',"51 تا 200 نفر"),('201-500',"201 تا 500 نفر"),('501-1000',"501 تا 1000 نفر"),('1000+',"بیش از 1000 نفر"))
    
    
    
    user = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name='کاربر',related_name='employer')
    persian_compnay_name = models.CharField(max_length=220,verbose_name="نام شرکت به فارسی")
    description = models.TextField(verbose_name="اطلاعاتی درمورد شرکت",null=True,blank=True)
    company_name = models.CharField(max_length=220,verbose_name="نام شرکت به انگلیسی")
    company_logo = models.ImageField(verbose_name='لوگو شرکت',null=True,blank=True,upload_to='images/company_logo')
    site_address = models.URLField(verbose_name='آدرس سایت شرکت',blank=True,null=True)
    company_filed = models.ForeignKey(to=CompanyActivity,max_length=220,verbose_name='حوزه فعالیت شرکت',on_delete=models.CASCADE)
    prson_count = models.CharField(max_length=120,choices=PERSON_COUNTER,verbose_name='تعداد پرسنل')
    verified_by_admin = models.BooleanField(verbose_name="تایید شده توسط ادمین",default=False)
    province = ProvinceField(verbose_name='نام استان')
    county = CountyField(verbose_name="نام شهرستان")
    district = models.ForeignKey(TehranDistrict,on_delete=models.CASCADE,verbose_name='نام منطقه',null=True,blank=True)

    def __str__(self):
        return f"{self.user.user_type} {self.company_name}"
    
    class Meta:
        verbose_name = 'کارفرما'
        verbose_name_plural = 'کارفرمایان'
    
class JobSeeker(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name='کاربر',related_name='jobseeker')
    job_category = models.ForeignKey(to=Job, verbose_name="شغل", on_delete=models.CASCADE)
    province = ProvinceField(verbose_name='نام استان')
    county = CountyField(verbose_name="نام شهرستان")
    district = models.ForeignKey(TehranDistrict,on_delete=models.CASCADE,verbose_name='نام منطقه',null=True,blank=True)

    
    
    class Meta:
        verbose_name = 'کارجو'
        verbose_name_plural = 'کارجویان'
        
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.job_category} , {self.county}"
    
