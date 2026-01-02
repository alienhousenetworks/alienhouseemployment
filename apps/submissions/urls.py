from django.urls import path
from . import views

app_name = 'submissions'

urlpatterns = [
    path('<int:task_id>/create/', views.SubmissionCreateView.as_view(), name='submission_create'),
    path('<int:pk>/review/', views.SubmissionReviewView.as_view(), name='submission_review'),
    path('<int:pk>/download/', views.SubmissionDownloadView.as_view(), name='submission_download'),
]
