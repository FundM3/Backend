from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
import requests
from main.utils.env_loader import env_loader

class CustomUserManager(BaseUserManager):
    def create_wallet_for_user(self, email):
        url = "https://contracts-api.owlprotocol.xyz/api/project/projectUser"
        payload = {"email": email}
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-api-key": env_loader.OWL_API_KEY
        }
        response = requests.post(url, json=payload, headers=headers).json()
        userId = response.get("userId")

        print(response)
        return userId
    
    def get_user_address(self, userId):
        chainId = 123420111
        url = f"https://contracts-api.owlprotocol.xyz/api/project/projectUser?chainId={chainId}&userId={userId}"
        headers = {
            "accept": "application/json",
            "x-api-key": env_loader.OWL_API_KEY
        }

        response = requests.get(url, headers=headers).json()
        safe_address = response.get("safeAddress")

        print(response)
        return safe_address

    def create_user(self, email, password=None, wallet_address=None, is_wallet_connected=False, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        
        if password:
            user.set_password(password)
        
        if not wallet_address and not is_wallet_connected:
            userId = self.create_wallet_for_user(email)
            wallet_address = self.get_user_address(userId)
        
        user.wallet_address = wallet_address
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    wallet_address = models.CharField(max_length=42, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name="customuser_groups",
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name="customuser_permissions",
        help_text='Specific permissions for this user.'
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
