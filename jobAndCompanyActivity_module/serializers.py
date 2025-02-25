from rest_framework.serializers import ModelSerializer

from jobAndCompanyActivity_module.models import Job,CompanyActivity



class JobSerializer(ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        
        
        
class CompanyActivitySerializer(ModelSerializer):
    class Meta:
        model = CompanyActivity
        fields = '__all__'
        