from django.db import models
from main.apps.user.models import CustomUser

def user_profile_img_path(instance, filename):
    extension = filename.split('.')[-1]
    filename = f"{instance.user.wallet_address}.{extension}"
    return f'profile_images/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255)
    profile_img = models.ImageField(upload_to=user_profile_img_path, null=True, blank=True)
    visible = models.BooleanField(default=False)
    x_url = models.URLField(max_length=200, blank=True, null=True)
    github_url = models.URLField(max_length=200, blank=True, null=True)
    telegram_url = models.URLField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.wallet_address

    @property
    def email(self):
        return self.user.email

    @property
    def address(self):
        return self.user.wallet_address
