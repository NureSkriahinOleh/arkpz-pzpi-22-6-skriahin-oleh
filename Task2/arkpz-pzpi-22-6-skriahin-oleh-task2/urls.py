from django.urls import path
from .views import IncidentReportListView, IncidentReportDetailView

urlpatterns = [
    path('incidents/', IncidentReportListView.as_view(), name='incident-list'),
    path('incidents/<int:pk>/', IncidentReportDetailView.as_view(), name='incident-detail'),
]