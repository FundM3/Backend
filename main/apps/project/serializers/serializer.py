from rest_framework import serializers
from django.utils import timezone
from main.apps.project.models import Project, ProjectImage
from main.apps.profile.models import Profile


class CreateProjectSerializer(serializers.ModelSerializer):
    project_images = serializers.ListField(
        child=serializers.ImageField(), 
        write_only=True, 
        required=False
    )

    class Meta:
        model = Project
        fields = ['project_name', 'tag_line', 'description', 'logo_img', 'x_url', 'github_url', 'telegram_url', 'website_url', 'discord_url', 'project_images']

    def create(self, validated_data):
        project_images = validated_data.pop('project_images', [])
        project = Project.objects.create(**validated_data)
        for img in project_images:
            ProjectImage.objects.create(project=project, image=img)
        return project

class LinkSerializer(serializers.Serializer):
    x = serializers.URLField(source='x_url')
    github = serializers.URLField(source='github_url')
    telegram = serializers.URLField(source='telegram_url')
    website = serializers.URLField(source='website_url')
    discord = serializers.URLField(source='discord_url')

class OwnerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    address = serializers.CharField(source='user.wallet_address')
    profile_img = serializers.ImageField(use_url=True)

    class Meta:
        model = Profile
        fields = ['name', 'email', 'address', 'profile_img']

class ProjectImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = ProjectImage
        fields = ['image']

class BaseProjectSerializer(serializers.ModelSerializer):
    elapsed_time = serializers.SerializerMethodField()
    logo_img = serializers.ImageField(use_url=True)
    owner = OwnerSerializer(source='user.profile', read_only=True)

    class Meta:
        model = Project
        fields = ['project_name', 'tag_line', 'logo_img', 'owner', 'elapsed_time']
    
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

class ProjectDetailSerializer(BaseProjectSerializer):
    link = LinkSerializer(source='*')
    project_img = serializers.SerializerMethodField()
    contribution_list = serializers.SerializerMethodField()

    class Meta(BaseProjectSerializer.Meta):
        fields = ['project_name', 'tag_line', 'description', 'logo_img', 'project_img', 'link', 'contribution_list', 'owner', 'elapsed_time']
        print('fields:\n', fields)

    def get_project_img(self, obj):
        return [img.image.url for img in obj.images.all()]

    def get_contribution_list(self, obj):
        return []

class ProjectListSerializer(BaseProjectSerializer):
    class Meta(BaseProjectSerializer.Meta):
        fields = BaseProjectSerializer.Meta.fields
