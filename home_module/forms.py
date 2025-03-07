from django import forms  
from django.forms import widgets
from iranian_cities.models import Province,County

from advertisement_module.models import ReportAdvertisment
from .models import TehranDistrict

class LocationForm(forms.Form):
    
    JOBTYPE = (("select","انتخاب"),("تمام وقت","تمام وقت"),("پاره وقت","پاره وقت"),("دورکاری","دورکاری"),("کارآموزی","کارآموزی"))

    
    province = forms.ModelChoiceField(queryset=Province.objects.all(),required=False,label="استان",empty_label="انتخاب استان",widget=widgets.Select(attrs={'class':'form-select'}))
    county = forms.ModelChoiceField(queryset=County.objects.all(),required=False,label="شهر",empty_label="انتخاب شهر",widget=widgets.Select(attrs={'class':'form-select','onchange':'Check_county(value)'}))
    district=forms.ModelChoiceField(queryset=TehranDistrict.objects.all(),required=False,label="منطقه",empty_label="انتخاب منطقه",widget=widgets.Select(attrs={'class':'form-select','hidden':''}))
    job_type = forms.ChoiceField(choices=JOBTYPE,label="نوع شغل",required=False,widget=widgets.Select(attrs={'class':'form-select'}))
    search = forms.CharField(max_length=220,required=False,widget=widgets.TextInput(attrs={'placeholder':"عنوان شغلی",'type':'text','class':'form-control'}))
    

class ReportModelForm(forms.ModelForm):
        class Meta:
            model = ReportAdvertisment
            fields = ['message','image']