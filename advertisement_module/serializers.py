from rest_framework import serializers

# New imports:
from .models import (
    Advertisement,
    AdvertisementJobSeeker,
    AdDisplayDuration,
    Skill,
    Subscription,
    ReportAdvertisment,
    JobHistory,
)



class SubscriptionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class SkillModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class AdDisplayDurationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdDisplayDuration
        fields = "__all__"


class JobHistoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobHistory
        fields = "__all__"


class AdvertisementModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        exclude = ['created_at', 'expire_date']


class AdvertisementJobSeekerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementJobSeeker
        exclude = ['created_at', 'expire_date']
