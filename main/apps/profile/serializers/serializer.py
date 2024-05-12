from rest_framework import serializers
from main.apps.profile.models import Profile


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'profile_img', 'visible', 'x_url', 'github_url', 'telegram_url']
        extra_kwargs = {'profile_img': {'required': False}}
