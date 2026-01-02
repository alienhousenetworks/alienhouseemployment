from django.urls import path
from .views import (
    EmployeeProductivityView, DepartmentAnalyticsView,
    TaskTrendsView, ExportReportView, ReportListCreateView,
    EmployeeAnalyticsView, ManagerAnalyticsView, DepartmentAnalyticsView as DeptAnalyticsView,
    AdminAnalyticsView, TemplateExportView
)

urlpatterns = [
    # API endpoints
    path('api/productivity/', EmployeeProductivityView.as_view(), name='employee-productivity'),
    path('api/department-analytics/', DepartmentAnalyticsView.as_view(), name='department-analytics'),
    path('api/task-trends/', TaskTrendsView.as_view(), name='task-trends'),
    path('api/export/<str:format_type>/', ExportReportView.as_view(), name='export-report'),
    path('api/reports/', ReportListCreateView.as_view(), name='report-list-create'),

    # Template-based views
    path('employee/', EmployeeAnalyticsView.as_view(), name='employee-analytics'),
    path('manager/', ManagerAnalyticsView.as_view(), name='manager-analytics'),
    path('department/', DeptAnalyticsView.as_view(), name='department-analytics'),
    path('admin/', AdminAnalyticsView.as_view(), name='admin-analytics'),

    # Template export
    path('export/<str:format_type>/<str:view_type>/', TemplateExportView.as_view(), name='export-template'),
]
