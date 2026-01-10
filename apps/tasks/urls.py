from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('create/', views.TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/accept/', views.TaskAcceptView.as_view(), name='task_accept'),
    path('list/', views.TaskListView.as_view(), name='task_list'),
    path('employee/dashboard/', views.EmployeeTaskDashboardView.as_view(), name='employee_dashboard'),
    path('manager/dashboard/', views.ManagerTaskDashboardView.as_view(), name='manager_dashboard'),
    path('<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/log-time/', views.TimeLogCreateView.as_view(), name='time_log_create'),
    path('reports/', views.TaskReportsView.as_view(), name='task_reports'),
]
