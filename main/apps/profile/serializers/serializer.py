from rest_framework import serializers
from django.utils import timezone
from main.apps.profile.models import Profile
from main.apps.project.models import Project
from main.apps.contribution.models import Contribution
from main.apps.contribution.serializers import ContributionListSerializer


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'profile_img', 'visible', 'x_url', 'github_url', 'telegram_url']
        extra_kwargs = {'profile_img': {'required': False}}

class LinkSerializer(serializers.Serializer):
    x = serializers.URLField(source='x_url')
    github = serializers.URLField(source='github_url')
    telegram = serializers.URLField(source='telegram_url')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'project_name', 'tag_line', 'logo_img']

class BaseProfileSerializer(serializers.ModelSerializer):
    link = LinkSerializer(source='*')
    elapsed_time = serializers.SerializerMethodField()
    profile_img = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = Profile
        fields = ['name', 'profile_img', 'link', 'elapsed_time']
    
    def get_elapsed_time(self, obj):
        now = timezone.now()
        diff = now - obj.created_at
        if diff.days >= 365:
            return f"{diff.days // 365} years ago"
        elif diff.days >= 30:
            return f"{diff.days // 30} months ago"
        elif diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds >= 3600:
            return f"{diff.seconds // 3600} hours ago"
        elif diff.seconds >= 60:
            return f"{diff.seconds // 60} minutes ago"
        else:
            return "Just now"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['address'] = instance.user.wallet_address
        return ret

class ProfileDetailSerializer(BaseProfileSerializer):
    project_of_user = serializers.SerializerMethodField()
    contribution_list = serializers.SerializerMethodField()

    class Meta(BaseProfileSerializer.Meta):
        fields =  ['name', 'email', 'address', 'profile_img', 'link', 'project_of_user', 'contribution_list', 'visible', 'elapsed_time']

    def get_project_of_user(self, obj):
        projects = Project.objects.filter(user__wallet_address=obj.user.wallet_address)
        return ProjectSerializer(projects, context={'request': self.context.get('request')}, many=True).data

    def get_contribution_list(self, obj):
        contribution_list = Contribution.objects.filter(receiver_address=obj.user.wallet_address)
        return ContributionListSerializer(contribution_list, context={'request': self.context.get('request')}, many=True).data

    def get_email(self, obj):
        return obj.user.email

class ProfileListSerializer(BaseProfileSerializer):
    class Meta(BaseProfileSerializer.Meta):
        fields = BaseProfileSerializer.Meta.fields
