from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views

urlpatterns = [
    path(
        "api/statistics/",
        views.Statistics.as_view(),
        name="api_statistics",
    ),
    path(
        "api/update-prom-metrics/",
        views.UpdatePromMetrics.as_view(),
        name="api_update_prom_metrics",
    ),
    path(
        "api/update-statistics/",
        views.UpdateStatistics.as_view(),
        name="api_update_statistics",
    ),
]
