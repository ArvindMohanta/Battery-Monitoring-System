from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BatteryViewSet, BatteryAlertViewSet, BatteryLogViewSet, BatteryDeviceViewSet
from .dashboard_views import (
    dashboard, dashboard_stats, battery_chart_data, battery_details, 
    alert_summary, battery_trend, dashboard_export
)

router = DefaultRouter()
router.register(r'batteries', BatteryViewSet, basename='battery')
router.register(r'alerts', BatteryAlertViewSet, basename='battery-alert')
router.register(r'logs', BatteryLogViewSet, basename='battery-log')
router.register(r'devices', BatteryDeviceViewSet, basename='battery-device')

urlpatterns = [
    path('', include(router.urls)),
    # Dashboard endpoints
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/stats/', dashboard_stats, name='dashboard-stats'),
    path('dashboard/chart-data/', battery_chart_data, name='chart-data'),
    path('dashboard/battery-details/', battery_details, name='battery-details'),
    path('dashboard/alerts/', alert_summary, name='alert-summary'),
    path('dashboard/trend/', battery_trend, name='battery-trend'),
    path('dashboard/export/', dashboard_export, name='dashboard-export'),
]
