from django.urls import path
from .views import create_project_view, get_project_view, get_project_list


urlpatterns = [
    path('project/create/', create_project_view, name='create-project'),
    path('project/list/', get_project_list, name='get-project-list'),
    path('project/<int:id>/', get_project_view, name='get-project-detail'),
]
