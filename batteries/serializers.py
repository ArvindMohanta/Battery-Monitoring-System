from rest_framework import serializers
from .models import Battery, BatteryAlert, BatteryLog, BatteryDevice


class BatterySerializer(serializers.ModelSerializer):
    """Serializer for Battery model."""
    
    class Meta:
        model = Battery
        fields = [
            'id', 'serial_number', 'battery_type', 'capacity', 'voltage_nominal',
            'current_charge', 'current_voltage', 'current_temperature', 'current_status',
            'health_percentage', 'cycle_count', 'max_discharge_current', 'max_charge_current',
            'last_updated', 'created_at'
        ]
        read_only_fields = ['id', 'last_updated', 'created_at']


class BatteryAlertSerializer(serializers.ModelSerializer):
    """Serializer for BatteryAlert model."""
    
    battery_serial = serializers.CharField(source='battery.serial_number', read_only=True)
    
    class Meta:
        model = BatteryAlert
        fields = [
            'id', 'battery', 'battery_serial', 'alert_type', 'alert_level',
            'message', 'is_resolved', 'created_at', 'resolved_at'
        ]
        read_only_fields = ['id', 'created_at', 'resolved_at']


class BatteryLogSerializer(serializers.ModelSerializer):
    """Serializer for BatteryLog model."""
    
    battery_serial = serializers.CharField(source='battery.serial_number', read_only=True)
    
    class Meta:
        model = BatteryLog
        fields = [
            'id', 'battery', 'battery_serial', 'charge_percentage', 'voltage',
            'temperature', 'current', 'status', 'logged_at'
        ]
        read_only_fields = ['id', 'logged_at']


class BatteryDeviceSerializer(serializers.ModelSerializer):
    """Serializer for BatteryDevice model."""
    
    batteries_detail = BatterySerializer(source='batteries', many=True, read_only=True)
    
    class Meta:
        model = BatteryDevice
        fields = [
            'id', 'device_name', 'device_type', 'serial_number', 'location',
            'batteries', 'batteries_detail', 'is_active', 'created_at', 'last_checked'
        ]
        read_only_fields = ['id', 'created_at']
