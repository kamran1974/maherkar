from rest_framework.serializers import ModelSerializer

from account_module.models import User, Employer, JobSeeker
from advertisement_module.models import Advertisement
from advertisement_module.serializers import JobHistoryModelSerializer, AdvertisementJobSeekerModelSerializer


class AdvertisementSerializer(ModelSerializer):
    """سریالایزر برای مدل Advertisement."""
    class Meta:
        model = Advertisement
        fields = "__all__"


class EmployerSerializer(ModelSerializer):
    """سریالایزر برای مدل Employer به همراه تبلیغات مربوطه."""
    advertisements = AdvertisementSerializer(many=True, read_only=True)
    
    class Meta:
        model = Employer
        fields = "__all__"


class JobSeekerSerializer(ModelSerializer):
    """سریالایزر برای مدل JobSeeker به همراه تبلیغات و تاریخچه شغلی."""
    advertisement = AdvertisementJobSeekerModelSerializer(read_only=True)
    job_histories = JobHistoryModelSerializer(many=True, read_only=True)
    
    class Meta:
        model = JobSeeker
        fields = "__all__"


class UserSerializer(ModelSerializer):
    """سریالایزر برای مدل User به همراه اطلاعات کارفرما و کارجو (در صورت وجود)."""
    employer = EmployerSerializer(read_only=True)
    jobseeker = JobSeekerSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = "__all__"
