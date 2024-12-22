from django.urls import path
from .views import CameraListView, CameraDetailView, CameraLogListView, CameraLogDetailView

urlpatterns = [
    # Ендпоінти для камер
    path('cameras/', CameraListView.as_view(), name='camera-list'),
    path('cameras/<int:pk>/', CameraDetailView.as_view(), name='camera-detail'),

    # Ендпоінти для логів камер
    path('cameras/<int:camera_id>/logs/', CameraLogListView.as_view(), name='camera-log-list'),
    path('cameras/logs/<int:pk>/', CameraLogDetailView.as_view(), name='camera-log-detail'),
]