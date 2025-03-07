from rest_framework.serializers import ModelSerializer

from account_module.models import User,Employer,JobSeeker
from advertisement_module.models import Advertisment
from advertisement_module.serializers import JobHistoryModelSerializer,AdvertisementJobSeekerModelSerializer

class AdvertismentSerializer(ModelSerializer):
    class Meta:
        model = Advertisment
        fields = "__all__"


class EmployerSerializer(ModelSerializer):
    advertisements = AdvertismentSerializer(many=True,read_only=True)
    
    class Meta:
        model = Employer
        fields = "__all__"
        
class JobSeekerSerializer(ModelSerializer):
    advertisement = AdvertisementJobSeekerModelSerializer(read_only=True)
    job_histories = JobHistoryModelSerializer(many=True,read_only = True)
    class Meta:
        model = JobSeeker
        fields = "__all__"

class UserSerializer(ModelSerializer):
    employer = EmployerSerializer(read_only=True)
    jobseeker =JobSeekerSerializer(read_only=True)
    class Meta:
        model = User
        fields = "__all__"