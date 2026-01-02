from rest_framework import serializers
from .models import KPI, Report, AnalyticsCache

class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class AnalyticsCacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsCache
        fields = '__all__'

# Custom serializers for analytics data
class ProductivitySerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    user_name = serializers.CharField()
    tasks_completed = serializers.IntegerField()
    tasks_overdue = serializers.IntegerField()
    average_completion_time = serializers.FloatField()
    productivity_score = serializers.FloatField()

class DepartmentAnalyticsSerializer(serializers.Serializer):
    department = serializers.CharField()
    total_employees = serializers.IntegerField()
    total_tasks = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    overdue_tasks = serializers.IntegerField()
    average_productivity = serializers.FloatField()

class TaskTrendsSerializer(serializers.Serializer):
    date = serializers.DateField()
    tasks_created = serializers.IntegerField()
    tasks_completed = serializers.IntegerField()
    tasks_overdue = serializers.IntegerField()
