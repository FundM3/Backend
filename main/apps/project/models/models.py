from django.db import models
from main.apps.user.models import CustomUser
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver


def project_directory_path(instance, filename):
    project_id = instance.project.pk if hasattr(instance, 'project') else instance.pk
    if isinstance(instance, Project):
        return f'projects/logo/{filename}'
    else:
        return f'projects/images/{project_id}/{filename}'

class Project(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects')
    project_name = models.CharField(max_length=255)
    tag_line = models.CharField(max_length=255)
    description = models.TextField()
    logo_img = models.ImageField(upload_to=project_directory_path, null=False, blank=False)
    x_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    telegram_url = models.URLField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    discord_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name

    @property
    def email(self):
        return self.user.email

    @property
    def owner(self):
        return self.user.wallet_address

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=project_directory_path)

@receiver(pre_save, sender=ProjectImage)
def limit_project_images(sender, instance, **kwargs):
    if instance._state.adding and ProjectImage.objects.filter(project=instance.project).count() >= 4:
        raise ValidationError('A project can have a maximum of 4 images.')
