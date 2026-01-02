from django.urls import path
from . import views

app_name = 'organization'

urlpatterns = [
    path('employee/dashboard/', views.EmployeeDashboardView.as_view(), name='employee_dashboard'),
    path('manager/dashboard/', views.ManagerDashboardView.as_view(), name='manager_dashboard'),
    # Add other organization URLs as needed
]
