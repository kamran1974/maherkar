from django.contrib import admin
from .models import (
    Advertisement,
    AdvertisementJobSeeker,
    AdDisplayDuration,
    Skill,
    Subscription,
    ReportAdvertisment,
    JobHistory
)


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['title', 'advertise_code', 'status', 'employer']
    fields = [
        'province', 'county', 'district', 'subscription', 'created_at', 'duration',
        'expire_date', 'pay_status', 'status', 'is_show', 'advertise_code', 'employer',
        'title', 'description_position', 'salary', 'job', "job_type", "type_of_cooperation",
        'gender', 'soldier_status', 'degree', 'skills', 'check_by_admin', 'display_total_price'
    ]
    readonly_fields = ['advertise_code', 'expire_date', 'display_total_price', 'created_at']
    list_filter = ['check_by_admin', 'is_show', 'pay_status']
    ordering = ['-created_at']
    autocomplete_fields = ['province', 'county']

    def display_total_price(self, obj):
        return f"{obj.total_price:,}"
    display_total_price.short_description = "مبلغ کل"


class AdvertisementJobSeekerAdmin(admin.ModelAdmin):
    list_display = ['advertise_code', 'status', 'jobSeeker']
    fields = [
        'province', 'county', 'district', 'subscription', 'created_at', 'duration',
        'expire_date', 'pay_status', 'status', 'display_total_price', 'is_show', 'advertise_code',
        'jobSeeker', 'gender', 'age', 'married_status', 'children_number', 'field_study',
        'history_injury', 'salary', 'job', "job_type", "insurance", 'soldier_status', 'degree',
        'skills', 'description', 'address', 'check_by_admin'
    ]
    readonly_fields = ['advertise_code', 'expire_date', 'display_total_price', 'created_at']
    list_filter = ['is_show', 'pay_status', 'check_by_admin']
    ordering = ['-created_at']
    autocomplete_fields = ['province', 'county']

    def display_total_price(self, obj):
        return f"{obj.total_price:,}"
    display_total_price.short_description = "مبلغ کل"


admin.site.register(AdDisplayDuration)
admin.site.register(Skill)
admin.site.register(Subscription)
admin.site.register(ReportAdvertisment)
# اگر مدل ReportAdvertismentJobSeeker وجود دارد، آن را نیز ثبت کنید:
# admin.site.register(ReportAdvertismentJobSeeker)
admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(AdvertisementJobSeeker, AdvertisementJobSeekerAdmin)
admin.site.register(JobHistory)
