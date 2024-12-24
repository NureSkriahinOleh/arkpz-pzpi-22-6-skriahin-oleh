from django.urls import path
from .views import *

urlpatterns = [
    path('admin/make-migrations/', MakeMigrationsView.as_view(), name='make-migrations'),
    path('admin/migrate/', MigrateView.as_view(), name='migrate'),
    path('admin/backup/', BackupDatabaseView.as_view(), name='backup-database'),
    path('admin/restore/', RestoreDatabaseView.as_view(), name='restore-database'),
]