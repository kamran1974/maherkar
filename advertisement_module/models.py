import random
from iranian_cities.fields import ProvinceField , CountyField
import jdatetime
from django.db import models
from django_jalali.db import models as jmodels

from account_module.models import Employer, User
from home_module.models import TehranDistrict
from jobAndCompanyActivity_module.models import Job


class Subscription(models.Model):
    name = models.CharField(verbose_name='نوع اشتراک',max_length=120,)
    price = models.IntegerField(default=0,verbose_name='قیمت',help_text='قیمت ها به تومان است - برای رایگان بودن تعرفه این بخش را نادیده بگیرید')
    
    def __str__(self):
        return f"{self.name} {self.price}"
    
    class Meta:
        verbose_name = 'تعرفه'
        verbose_name_plural = 'تعرفه ها'
    
class Skill(models.Model):
    name = models.CharField(max_length=220,verbose_name='مهارت های کارجو')
    
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = 'مهارت'
        verbose_name_plural = 'مهارت ها'
    
    
class Duration(models.Model):
    day = models.IntegerField(verbose_name="روز",help_text='برای مثال 4')
    price = models.IntegerField(verbose_name='قیمت',help_text='این قیمت کل هست -مثلا برای 7 روز کلا 7000 - قیمت ها به تومان است')
    
    class Meta:
        verbose_name = 'زمان نمایش آگهی'
        verbose_name_plural = 'زمان نمایش آگهی ها'
    
    def __str__(self):
        return f"{self.day}روز - {self.price:,} تومان"


 
class Advertisment(models.Model):
    GENDER = (('مرد','مرد'),('زن','زن'))
    SOLDIER_STATUS = (('پایان خدمت','پایان خدمت'),('معافیت دائم','معافیت دائم'),('معافیت تحصیلی',"معافیت تحصیلی"))
    DEGREE = (("مهم نیست","مهم نیست"),('زیر دیپلم','زیر دیپلم'),('دیپلم','دیپلم'),('فوق دیپلم','فوق دیپلم'),('لیسانس','لیسانس'),('فوق لیسانس','فوق لیسانس'),('دکترا','دکترا'))
    TYPEOFCOOPERATION = (("مهم نیست","مهم نیست"),('کمتر از 3 سال','کمتر از 3 سال'),("3 تا 6 سال","3 تا 6 سال"),("بیشتر از 6 سال","بیشتر از 6 سال"))
    JOBTYPE = (("تمام وقت","تمام وقت"),("پاره وقت","پاره وقت"),("دورکاری","دورکاری"),("کارآموزی","کارآموزی"))
    STATUS = (("unpaid","در انتظار پرداخت"),("pending","درحال بررسی"),("approved","تایید شده"),("rejected","رد شده"))
    
    employer = models.ForeignKey(Employer,on_delete=models.CASCADE,verbose_name='کارفرما',related_name='advertisements')
    advertise_code = models.CharField(max_length=220,unique=True,db_index=True,verbose_name='کدآگهی',help_text='بعد از ثبت مقدار دهی می شود')
    title = models.CharField(max_length=220,verbose_name="عنوان آگهی")
    description_position = models.TextField(verbose_name='موقعیت شغلی')
    gender = models.CharField(max_length=120,verbose_name='جنسیت',choices=GENDER)
    soldier_status = models.CharField(max_length=120,verbose_name='وضعیت سربازی',choices=SOLDIER_STATUS)
    degree =models.CharField(max_length=120,verbose_name='حداقل مدرک تحصیلی',choices=DEGREE)
    type_of_cooperation = models.CharField(max_length=220,choices=TYPEOFCOOPERATION,verbose_name="سابقه کار مرتبط")
    salary = models.CharField(verbose_name="حداقل دستمزد",max_length=220,help_text="درصورت خالی گذاشتن ای بخش مبلغ دستمزد توافقی می شود")
    created_at = jmodels.jDateTimeField(verbose_name='تاریخ ثبت',help_text='بعد از ثبت مقدار دهی می شود',null=True,blank=True)
    expire_date = jmodels.jDateTimeField(verbose_name='تاریخ انقضا',null=True,blank=True,help_text='به صورت خودکار محاسبه می شود')
    total_price = models.IntegerField(verbose_name='جمع کل',default=0,help_text='به صورت خودکار محاسبه می شود')
    pay_status = models.BooleanField(verbose_name='وضعیت پرداخت',default=False)
    check_by_admin = models.BooleanField(verbose_name=' مشاهده  شده توسط ادمین',default=False)
    is_show = models.BooleanField(verbose_name='نمایش داده شود / نشود',default=False)
    status = models.CharField(max_length=220,verbose_name="وضعیت",choices=STATUS,default="unpaid")
    job_type = models.CharField(max_length=220,verbose_name='نوع شغل',choices=JOBTYPE)
    
    province = ProvinceField(verbose_name='نام استان')
    county = CountyField(verbose_name="نام شهرستان")
    district = models.ForeignKey(TehranDistrict,on_delete=models.CASCADE,verbose_name='نام منطقه',null=True,blank=True)
    
    job = models.ForeignKey(Job,on_delete=models.CASCADE,verbose_name='شغل',related_name='advertisements')
    subscription = models.ForeignKey(Subscription,on_delete=models.PROTECT,related_name='advertisements',verbose_name='نوع اشتراک')
    duration = models.ForeignKey(Duration,on_delete=models.CASCADE,related_name='advertisements',verbose_name='زمان نمایش')
    skills = models.ManyToManyField(Skill,related_name='advertisements',verbose_name='مهارت های کارجو',null=True,blank=True)
    
    
    
    def __str__(self):
        return f"{self.advertise_code} - {self.employer.user}"
    
    
    class Meta:
        verbose_name = 'آگهی'
        verbose_name_plural = 'آگهی ها'
    
    def save(self, *args,**kwargs):
        if self.salary == "" or None:
            self.salary = "توافقی"
        if not self.pk:
            
        
            self.advertise_code = random.randint(10000000,99999999)
        
            self.total_price = self.subscription.price + self.duration.price
        
            self.created_at = jdatetime.datetime.now().replace(microsecond=0)
        
        
            day = self.duration.day
            self.expire_date = self.created_at + jdatetime.timedelta(days=day)
        
        
        return super().save(args,kwargs)

    

class ReportAdvertisment(models.Model):
    STATUS = (("0","درحال بررسی"),("1","تایید شده"),("2","رد شده"))
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='کاربر')
    message = models.TextField(verbose_name='پیام')
    image = models.ImageField(verbose_name='عکس',upload_to="images/report",null=True,blank=True,help_text="در صورت وجود عکس آپلود کنید در غیر این صورت نادیده بگیرید")
    status = models.CharField(max_length=220,verbose_name="وضعیت",choices=STATUS,default="0")
    created_at = jmodels.jDateTimeField(verbose_name='تاریخ ثبت',help_text='بعد از ثبت مقدار دهی می شود',null=True,blank=True)
    advertisment = models.ForeignKey(Advertisment,on_delete=models.CASCADE,verbose_name='آگهی',related_name='reports')

    class Meta:
        verbose_name = "گزارش"
        verbose_name_plural = "گزارش ها"
    
    def __str__(self):
        return self.message
    
    def save(self,*args,**kwargs):
        self.created_at = jdatetime.datetime.now().replace(microsecond=0)
        return super().save(args,kwargs)