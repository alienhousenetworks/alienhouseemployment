from django.urls import path
from . import views

app_name = 'organization'

urlpatterns = [
    path('employee/dashboard/', views.EmployeeDashboardView.as_view(), name='employee_dashboard'),
    path('manager/dashboard/', views.ManagerDashboardView.as_view(), name='manager_dashboard'),
    path('employee-list/', views.EmployeeListView.as_view(), name='employee-list'),
    # Add other organization URLs as needed
     path('assign-manager/<int:pk>/', views.AssignManagerView.as_view(), name='assign_manager'),
]

