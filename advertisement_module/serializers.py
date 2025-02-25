from rest_framework.serializers import ModelSerializer

from account_module.serializers import EmployerSerializer
from advertisement_module.models import Advertisment, Duration, Skill, Subscription





class SubscriptionModelSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
        
class SkillModelSerializer(ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"
        
class DurationModelSerializer(ModelSerializer):
    class Meta:
        model = Duration
        fields = "__all__"

class AdvertisementModelSerializer(ModelSerializer):
    employer = EmployerSerializer(read_only=True)
    class Meta:
        model = Advertisment
        exclude = ['created_at','expire_date']