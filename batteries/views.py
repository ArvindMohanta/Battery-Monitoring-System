from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from .models import Battery, BatteryAlert, BatteryLog, BatteryDevice
from .serializers import BatterySerializer, BatteryAlertSerializer, BatteryLogSerializer, BatteryDeviceSerializer


class BatteryViewSet(viewsets.ModelViewSet):
    """ViewSet for Battery model with custom actions."""
    
    queryset = Battery.objects.all()
    serializer_class = BatterySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['serial_number', 'battery_type']
    ordering_fields = ['current_charge', 'health_percentage', 'created_at']
    ordering = ['-last_updated']
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update battery status and readings."""
        battery = self.get_object()
        
        # Update battery data from request
        if 'current_charge' in request.data:
            battery.current_charge = request.data['current_charge']
        if 'current_voltage' in request.data:
            battery.current_voltage = request.data['current_voltage']
        if 'current_temperature' in request.data:
            battery.current_temperature = request.data['current_temperature']
        if 'current_status' in request.data:
            battery.current_status = request.data['current_status']
        
        battery.save()
        
        # Create log entry
        BatteryLog.objects.create(
            battery=battery,
            charge_percentage=battery.current_charge,
            voltage=battery.current_voltage,
            temperature=battery.current_temperature,
            current=request.data.get('current', 0),
            status=battery.current_status
        )
        
        # Check for alerts
        self._check_battery_alerts(battery)
        
        return Response(BatterySerializer(battery).data)
    
    @action(detail=True, methods=['get'])
    def health_report(self, request, pk=None):
        """Get detailed health report for a battery."""
        battery = self.get_object()
        recent_logs = battery.logs.all()[:100]
        recent_alerts = battery.alerts.filter(is_resolved=False)
        
        report = {
            'battery': BatterySerializer(battery).data,
            'recent_alerts': BatteryAlertSerializer(recent_alerts, many=True).data,
            'recent_readings': BatteryLogSerializer(recent_logs, many=True).data,
            'average_temperature': sum(log.temperature for log in recent_logs) / len(recent_logs) if recent_logs else 0,
        }
        
        return Response(report)
    
    @action(detail=False, methods=['get'])
    def low_health_batteries(self, request):
        """Get all batteries with low health."""
        health_threshold = request.query_params.get('threshold', 80)
        batteries = Battery.objects.filter(health_percentage__lt=float(health_threshold))
        serializer = self.get_serializer(batteries, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def critical_status_batteries(self, request):
        """Get all batteries with critical status."""
        batteries = Battery.objects.filter(current_status='FAULT')
        serializer = self.get_serializer(batteries, many=True)
        return Response(serializer.data)
    
    def _check_battery_alerts(self, battery):
        """Check battery parameters and create alerts if needed."""
        alerts_to_create = []
        
        # Check charge level
        if battery.current_charge < 10:
            alerts_to_create.append({
                'alert_type': 'LOW_CHARGE',
                'alert_level': 'WARNING',
                'message': f'Battery charge is critically low: {battery.current_charge}%'
            })
        
        # Check temperature
        if battery.current_temperature > 50:
            alerts_to_create.append({
                'alert_type': 'OVER_TEMPERATURE',
                'alert_level': 'CRITICAL',
                'message': f'Battery temperature is too high: {battery.current_temperature}°C'
            })
        
        # Check voltage
        if battery.current_voltage < battery.voltage_nominal * 0.8:
            alerts_to_create.append({
                'alert_type': 'UNDER_VOLTAGE',
                'alert_level': 'ERROR',
                'message': f'Battery voltage is too low: {battery.current_voltage}V'
            })
        
        # Check health
        if battery.health_percentage < 20:
            alerts_to_create.append({
                'alert_type': 'HEALTH_DEGRADATION',
                'alert_level': 'WARNING',
                'message': f'Battery health has degraded: {battery.health_percentage}%'
            })
        
        # Create alerts
        for alert_data in alerts_to_create:
            BatteryAlert.objects.create(battery=battery, **alert_data)


class BatteryAlertViewSet(viewsets.ModelViewSet):
    """ViewSet for BatteryAlert model."""
    
    queryset = BatteryAlert.objects.all()
    serializer_class = BatteryAlertSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['alert_type', 'battery__serial_number']
    ordering_fields = ['created_at', 'alert_level']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Mark an alert as resolved."""
        alert = self.get_object()
        alert.is_resolved = True
        alert.resolved_at = timezone.now()
        alert.save()
        return Response(BatteryAlertSerializer(alert).data)
    
    @action(detail=False, methods=['get'])
    def unresolved(self, request):
        """Get all unresolved alerts."""
        alerts = BatteryAlert.objects.filter(is_resolved=False)
        serializer = self.get_serializer(alerts, many=True)
        return Response(serializer.data)


class BatteryLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for BatteryLog model (read-only)."""
    
    queryset = BatteryLog.objects.all()
    serializer_class = BatteryLogSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['battery__serial_number']
    ordering_fields = ['logged_at']
    ordering = ['-logged_at']


class BatteryDeviceViewSet(viewsets.ModelViewSet):
    """ViewSet for BatteryDevice model."""
    
    queryset = BatteryDevice.objects.all()
    serializer_class = BatteryDeviceSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['device_name', 'serial_number']
    ordering_fields = ['device_name', 'created_at']
    ordering = ['device_name']
    
    @action(detail=True, methods=['get'])
    def battery_status(self, request, pk=None):
        """Get status of all batteries in this device."""
        device = self.get_object()
        batteries = device.batteries.all()
        serializer = BatterySerializer(batteries, many=True)
        return Response({
            'device': BatteryDeviceSerializer(device).data,
            'batteries': serializer.data
        })
