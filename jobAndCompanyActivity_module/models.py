from django.db import models
# Create your models here.
class Job(models.Model):
    job_category = models.CharField(max_length=220,unique=True,verbose_name='دسته بندی شغل',help_text='حوزه ای که کارجو در آن فعالیت میکند')
    
    
    def __str__(self):
        return f"{self.job_category}"
    
    class Meta:
        verbose_name = 'شغل'
        verbose_name_plural = 'مشاغل'
        
        
class CompanyActivity(models.Model):
    activity_name = models.CharField(max_length=220,unique=True,verbose_name='حوزه فعالیت',help_text='حوزه فعالیت شرکت')
    
    
    def __str__(self):
        return f"{self.activity_name}"
    
    class Meta:
        verbose_name = 'حوزه فعالیت شرکت'
        verbose_name_plural = 'حوزه های فعالیت شرکت ها'
        
