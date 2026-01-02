from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project_list'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('<int:project_id>/milestone/create/', views.MilestoneCreateView.as_view(), name='milestone_create'),
    path('templates/', views.ProjectTemplateListView.as_view(), name='template_list'),
    path('templates/create/', views.ProjectTemplateCreateView.as_view(), name='template_create'),
    path('templates/<int:template_id>/instantiate/', views.instantiate_project_from_template, name='instantiate_template'),
    path('<int:project_id>/resource/create/', views.ResourceAllocationCreateView.as_view(), name='resource_create'),
]
