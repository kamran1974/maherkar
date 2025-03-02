from django import forms
from .models import Advertisment,ReportAdvertisment



class AdvertisementModelForm(forms.ModelForm):
    class Meta:
        model = Advertisment
        exclude = ['employer','advertise_code','created_at','expire_date','pay_status','check_by_admin','status','is_show','total_price','province','county','district']

        
class UpdateAdvertisementModelForm(forms.ModelForm):
    class Meta:
        model = Advertisment
        exclude = ['employer','advertise_code','created_at','expire_date','pay_status','check_by_admin','status','is_show','total_price','province','county','district']
        
        
        
