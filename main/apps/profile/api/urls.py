from django.urls import path
from .views import update_profile_view


urlpatterns = [
    path('profile/update/', update_profile_view, name='update-profile'),
]
