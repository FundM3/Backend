from django.urls import path
from .views import record_contribution_view, get_contribution_list


urlpatterns = [
    path('contribution/record/', record_contribution_view, name='record-project'),
    path('contribution/<str:address>/', get_contribution_list, name='get-contribution-list'),
]
