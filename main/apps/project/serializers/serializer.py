from rest_framework import serializers
from main.apps.project.models import Project, ProjectImage


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
        logo_img = validated_data.pop('logo_img', [])
        project_images = validated_data.pop('project_images', [])
        project = Project.objects.create(**validated_data)


        for img in project_images:
            ProjectImage.objects.create(project=project, image=img)
        return project
