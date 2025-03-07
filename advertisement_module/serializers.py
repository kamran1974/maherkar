from rest_framework.serializers import ModelSerializer

from advertisement_module.models import Advertisment, Duration, Skill, Subscription,JobHistory,AdvertismentJobSeeker





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

class JobHistoryModelSerializer(ModelSerializer):
    class Meta:
        model = JobHistory
        fields = "__all__"

class AdvertisementModelSerializer(ModelSerializer):
    class Meta:
        model = Advertisment
        exclude = ['created_at','expire_date']
        
class AdvertisementJobSeekerModelSerializer(ModelSerializer):

    class Meta:
        model = AdvertismentJobSeeker
        exclude = ['created_at','expire_date']
