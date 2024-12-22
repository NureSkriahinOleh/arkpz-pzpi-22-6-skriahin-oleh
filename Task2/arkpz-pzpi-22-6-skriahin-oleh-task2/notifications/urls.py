from django.urls import path
from .views import NotificationListView, NotificationDetailView

urlpatterns = [
    # Ендпоінти для сповіщень
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
]