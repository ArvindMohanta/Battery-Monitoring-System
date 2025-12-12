from django.contrib import admin
from .models import Battery, BatteryAlert, BatteryLog, BatteryDevice


@admin.register(Battery)
class BatteryAdmin(admin.ModelAdmin):
    list_display = [
        'serial_number', 'battery_type', 'current_charge', 'current_status',
        'health_percentage', 'current_temperature', 'last_updated'
    ]
    list_filter = ['battery_type', 'current_status', 'health_percentage']
    search_fields = ['serial_number', 'battery_type']
    readonly_fields = ['created_at', 'last_updated']
    
    fieldsets = (
        ('Battery Information', {
            'fields': ('serial_number', 'battery_type', 'capacity', 'voltage_nominal')
        }),
        ('Current Status', {
            'fields': ('current_charge', 'current_voltage', 'current_temperature', 'current_status')
        }),
        ('Health Metrics', {
            'fields': ('health_percentage', 'cycle_count')
        }),
        ('Specifications', {
            'fields': ('max_discharge_current', 'max_charge_current')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'last_updated'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BatteryAlert)
class BatteryAlertAdmin(admin.ModelAdmin):
    list_display = ['battery', 'alert_type', 'alert_level', 'is_resolved', 'created_at']
    list_filter = ['alert_type', 'alert_level', 'is_resolved', 'created_at']
    search_fields = ['battery__serial_number', 'message']
    readonly_fields = ['created_at', 'resolved_at']


@admin.register(BatteryLog)
class BatteryLogAdmin(admin.ModelAdmin):
    list_display = ['battery', 'charge_percentage', 'voltage', 'temperature', 'status', 'logged_at']
    list_filter = ['battery', 'status', 'logged_at']
    search_fields = ['battery__serial_number']
    readonly_fields = ['logged_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(BatteryDevice)
class BatteryDeviceAdmin(admin.ModelAdmin):
    list_display = ['device_name', 'device_type', 'serial_number', 'is_active', 'created_at']
    list_filter = ['device_type', 'is_active', 'created_at']
    search_fields = ['device_name', 'serial_number', 'location']
    filter_horizontal = ['batteries']
    readonly_fields = ['created_at']
