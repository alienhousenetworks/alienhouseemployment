from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    
    # Add other organization URLs as needed
     path('', views.home_view, name='home_view'),
]
