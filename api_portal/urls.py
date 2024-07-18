from django.urls import path, include
from .views import *








urlpatterns = [
    path('api/dataset/', APIDatasetView.as_view(), name="api_dataset"),
    path('api/dataset/file/', APIDatasetFileView.as_view(), name="api_dataset_file"),
  
]