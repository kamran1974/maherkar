from django.contrib import admin
from .models import Advertisment,Duration,Skill,Subscription,ReportAdvertisment


class AdvertismentAdmin(admin.ModelAdmin):
    list_display = ['title','advertise_code','status','employer']
    fields = ['advertise_code','employer','title','description_position','province','county','district','job',"job_type","type_of_cooperation",'subscription','created_at','duration','expire_date','gender','soldier_status','degree','skills','check_by_admin','is_show','pay_status','status','display_total_price']
    readonly_fields = ['advertise_code','expire_date',"display_total_price",'created_at']
    list_filter = ['check_by_admin','is_show','pay_status',]
    ordering = ['-created_at']
    autocomplete_fields = ['province','county']        
    def display_total_price(self,obj):
        return f"{obj.total_price:,}"
    display_total_price.short_description = "مبلغ کل"


admin.site.register(Duration)
admin.site.register(Skill)
admin.site.register(Subscription)
admin.site.register(ReportAdvertisment)
admin.site.register(Advertisment,AdvertismentAdmin)

