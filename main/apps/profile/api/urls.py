from django.urls import path
from .views import update_profile_view, get_profile_view, get_profile_list


urlpatterns = [
    path('profile/update/', update_profile_view, name='update-profile'),
    path('profile/list/', get_profile_list, name='get-profile-list'),
    path('profile/<str:address>/', get_profile_view, name='get-profile'),
]
