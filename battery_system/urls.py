"""
URL configuration for battery_system project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from batteries.dashboard_views import dashboard

def welcome(request):
    """Welcome page showing API documentation."""
    return JsonResponse({
        'message': 'Welcome to Battery Management System',
        'documentation': {
            'dashboard': '/dashboard/',
            'admin': '/admin/',
            'api': '/api/',
            'api_endpoints': {
                'batteries': '/api/batteries/',
                'alerts': '/api/alerts/',
                'logs': '/api/logs/',
                'devices': '/api/devices/',
                'dashboard_stats': '/api/dashboard/stats/',
                'chart_data': '/api/dashboard/chart-data/',
                'battery_details': '/api/dashboard/battery-details/',
                'alerts_summary': '/api/dashboard/alerts/',
                'battery_trends': '/api/dashboard/trend/',
            }
        },
        'features': [
            'Real-time battery monitoring',
            'Interactive analytics dashboard',
            'Alert management',
            'Historical data logging',
            'Device management',
            'Complete REST API'
        ]
    })

urlpatterns = [
    path('', welcome, name='welcome'),
    path('dashboard/', dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path('api/', include('batteries.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

