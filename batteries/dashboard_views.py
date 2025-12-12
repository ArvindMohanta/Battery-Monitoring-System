from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Avg, Count, Q
from .models import Battery, BatteryAlert, BatteryLog, BatteryDevice
import json


def dashboard(request):
    """Battery management dashboard."""
    return render(request, 'batteries/dashboard.html')


def dashboard_stats(request):
    """API endpoint for dashboard statistics."""
    
    # Battery stats
    total_batteries = Battery.objects.count()
    active_batteries = Battery.objects.filter(current_status__in=['CHARGING', 'DISCHARGING']).count()
    faulty_batteries = Battery.objects.filter(current_status='FAULT').count()
    
    # Health stats
    avg_health = Battery.objects.aggregate(Avg('health_percentage'))['health_percentage__avg'] or 0
    low_health_count = Battery.objects.filter(health_percentage__lt=50).count()
    
    # Charge stats
    avg_charge = Battery.objects.aggregate(Avg('current_charge'))['current_charge__avg'] or 0
    
    # Temperature stats
    avg_temp = Battery.objects.aggregate(Avg('current_temperature'))['current_temperature__avg'] or 0
    
    # Alert stats
    total_alerts = BatteryAlert.objects.count()
    unresolved_alerts = BatteryAlert.objects.filter(is_resolved=False).count()
    critical_alerts = BatteryAlert.objects.filter(alert_level='CRITICAL', is_resolved=False).count()
    
    # Device stats
    total_devices = BatteryDevice.objects.count()
    active_devices = BatteryDevice.objects.filter(is_active=True).count()
    
    return JsonResponse({
        'batteries': {
            'total': total_batteries,
            'active': active_batteries,
            'faulty': faulty_batteries,
        },
        'health': {
            'average': round(avg_health, 2),
            'low_count': low_health_count,
        },
        'charge': {
            'average': round(avg_charge, 2),
        },
        'temperature': {
            'average': round(avg_temp, 2),
        },
        'alerts': {
            'total': total_alerts,
            'unresolved': unresolved_alerts,
            'critical': critical_alerts,
        },
        'devices': {
            'total': total_devices,
            'active': active_devices,
        }
    })


def battery_chart_data(request):
    """Get battery data for charts."""
    
    batteries = Battery.objects.all()
    
    # Status distribution
    status_data = Battery.objects.values('current_status').annotate(count=Count('id'))
    
    # Health distribution
    health_ranges = {
        'Excellent (90-100%)': Battery.objects.filter(health_percentage__gte=90).count(),
        'Good (70-89%)': Battery.objects.filter(health_percentage__gte=70, health_percentage__lt=90).count(),
        'Fair (50-69%)': Battery.objects.filter(health_percentage__gte=50, health_percentage__lt=70).count(),
        'Poor (<50%)': Battery.objects.filter(health_percentage__lt=50).count(),
    }
    
    # Charge levels
    charge_ranges = {
        'Full (90-100%)': Battery.objects.filter(current_charge__gte=90).count(),
        'High (70-89%)': Battery.objects.filter(current_charge__gte=70, current_charge__lt=90).count(),
        'Medium (40-69%)': Battery.objects.filter(current_charge__gte=40, current_charge__lt=70).count(),
        'Low (10-39%)': Battery.objects.filter(current_charge__gte=10, current_charge__lt=40).count(),
        'Critical (<10%)': Battery.objects.filter(current_charge__lt=10).count(),
    }
    
    # Battery types
    type_data = Battery.objects.values('battery_type').annotate(count=Count('id'))
    
    # Cycle count distribution
    cycles_ranges = {
        'New (0-100)': Battery.objects.filter(cycle_count__lte=100).count(),
        'Good (100-500)': Battery.objects.filter(cycle_count__gt=100, cycle_count__lte=500).count(),
        'Aging (500-1000)': Battery.objects.filter(cycle_count__gt=500, cycle_count__lte=1000).count(),
        'Old (1000+)': Battery.objects.filter(cycle_count__gt=1000).count(),
    }
    
    return JsonResponse({
        'status': list(status_data),
        'health_ranges': health_ranges,
        'charge_ranges': charge_ranges,
        'types': list(type_data),
        'cycle_ranges': cycles_ranges,
    })


def battery_details(request):
    """Get detailed battery information."""
    
    batteries = Battery.objects.all().values(
        'id', 'serial_number', 'battery_type', 'current_charge', 
        'current_voltage', 'current_temperature', 'current_status', 
        'health_percentage', 'cycle_count'
    )
    
    return JsonResponse({
        'batteries': list(batteries)
    })


def alert_summary(request):
    """Get alert summary data."""
    
    # Alert types breakdown
    alert_types = BatteryAlert.objects.values('alert_type').annotate(count=Count('id'))
    
    # Alert levels breakdown
    alert_levels = BatteryAlert.objects.values('alert_level').annotate(
        count=Count('id'),
        unresolved=Count('id', filter=Q(is_resolved=False))
    )
    
    # Recent unresolved alerts
    recent_alerts = BatteryAlert.objects.filter(is_resolved=False).select_related('battery').values(
        'id', 'battery__serial_number', 'alert_type', 'alert_level', 'message', 'created_at'
    ).order_by('-created_at')[:10]
    
    return JsonResponse({
        'alert_types': list(alert_types),
        'alert_levels': list(alert_levels),
        'recent_unresolved': list(recent_alerts),
    })


def battery_trend(request):
    """Get battery trend data from logs."""
    
    battery_id = request.GET.get('battery_id')
    
    if battery_id:
        logs = BatteryLog.objects.filter(battery_id=battery_id).order_by('logged_at')[:100]
    else:
        logs = BatteryLog.objects.all().order_by('logged_at')[:100]
    
    data = {
        'timestamps': [log.logged_at.isoformat() for log in logs],
        'charge': [log.charge_percentage for log in logs],
        'voltage': [log.voltage for log in logs],
        'temperature': [log.temperature for log in logs],
    }
    
    return JsonResponse(data)


def dashboard_export(request):
    """Export dashboard data as JSON for external use."""
    
    stats = dashboard_stats(request).json()
    chart_data = battery_chart_data(request).json()
    battery_data = battery_details(request).json()
    alert_data = alert_summary(request).json()
    
    return JsonResponse({
        'timestamp': __import__('django.utils.timezone', fromlist=['now']).now().isoformat(),
        'stats': stats,
        'charts': chart_data,
        'batteries': battery_data,
        'alerts': alert_data,
    })
