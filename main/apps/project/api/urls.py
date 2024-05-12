from django.urls import path
from .views import create_project_view


urlpatterns = [
    path('project/create/', create_project_view, name='create-project'),
]
