from django import forms
from .models import Advertisement, ReportAdvertisment, JobHistory, AdvertisementJobSeeker


class AdvertisementModelForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        exclude = [
            'employer',
            'advertise_code',
            'created_at',
            'expire_date',
            'pay_status',
            'check_by_admin',
            'status',
            'is_show',
            'total_price',
            'province',
            'county',
            'district'
        ]


class UpdateAdvertisementModelForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        exclude = [
            'employer',
            'advertise_code',
            'created_at',
            'expire_date',
            'pay_status',
            'check_by_admin',
            'status',
            'is_show',
            'total_price',
            'province',
            'county',
            'district'
        ]


class JobHistoryModelForm(forms.ModelForm):
    class Meta:
        model = JobHistory
        exclude = ['job_seeker']


class JobSeekerAdvertisementModelForm(forms.ModelForm):
    class Meta:
        model = AdvertisementJobSeeker
        exclude = [
            'jobSeeker',
            'advertise_code',
            'created_at',
            'expire_date',
            'pay_status',
            'check_by_admin',
            'status',
            'is_show',
            'total_price',
            'province',
            'county',
            'district'
        ]
        widgets = {
            'gender': forms.widgets.Select(attrs={'onchange': "check_gender(this)"})
        }
