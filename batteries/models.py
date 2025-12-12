from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Battery(models.Model):
    """Model representing a battery in the system."""
    
    STATUS_CHOICES = [
        ('CHARGING', 'Charging'),
        ('DISCHARGING', 'Discharging'),
        ('IDLE', 'Idle'),
        ('FAULT', 'Fault'),
    ]
    
    serial_number = models.CharField(max_length=100, unique=True)
    battery_type = models.CharField(max_length=50)  # Li-ion, NiMH, Lead-acid, etc.
    capacity = models.FloatField(help_text="Battery capacity in mAh")
    voltage_nominal = models.FloatField(help_text="Nominal voltage in volts")
    
    # Current status
    current_charge = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Current charge percentage (0-100%)"
    )
    current_voltage = models.FloatField(help_text="Current voltage in volts")
    current_temperature = models.FloatField(help_text="Temperature in Celsius")
    current_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IDLE')
    
    # Health metrics
    health_percentage = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=100,
        help_text="Battery health percentage (0-100%)"
    )
    cycle_count = models.IntegerField(default=0, help_text="Number of charge cycles")
    
    # Specifications
    max_discharge_current = models.FloatField(help_text="Max discharge current in Amps")
    max_charge_current = models.FloatField(help_text="Max charge current in Amps")
    
    # Timestamps
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-last_updated']
        verbose_name = 'Battery'
        verbose_name_plural = 'Batteries'
    
    def __str__(self):
        return f"{self.battery_type} - {self.serial_number}"


class BatteryAlert(models.Model):
    """Model for battery alerts and anomalies."""
    
    ALERT_LEVEL_CHOICES = [
        ('INFO', 'Information'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    ]
    
    ALERT_TYPE_CHOICES = [
        ('LOW_CHARGE', 'Low Charge'),
        ('OVERCHARGE', 'Overcharge'),
        ('OVER_TEMPERATURE', 'Over Temperature'),
        ('UNDER_VOLTAGE', 'Under Voltage'),
        ('OVER_CURRENT', 'Over Current'),
        ('HEALTH_DEGRADATION', 'Health Degradation'),
        ('FAULT', 'Fault Detected'),
        ('COMMUNICATION_ERROR', 'Communication Error'),
    ]
    
    battery = models.ForeignKey(Battery, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=30, choices=ALERT_TYPE_CHOICES)
    alert_level = models.CharField(max_length=20, choices=ALERT_LEVEL_CHOICES)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Battery Alert'
        verbose_name_plural = 'Battery Alerts'
    
    def __str__(self):
        return f"{self.get_alert_type_display()} - {self.battery.serial_number}"


class BatteryLog(models.Model):
    """Model for logging battery data history."""
    
    battery = models.ForeignKey(Battery, on_delete=models.CASCADE, related_name='logs')
    charge_percentage = models.FloatField()
    voltage = models.FloatField()
    temperature = models.FloatField()
    current = models.FloatField(help_text="Positive for charging, negative for discharging")
    status = models.CharField(max_length=20)
    logged_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-logged_at']
        verbose_name = 'Battery Log'
        verbose_name_plural = 'Battery Logs'
        indexes = [
            models.Index(fields=['battery', '-logged_at']),
        ]
    
    def __str__(self):
        return f"{self.battery.serial_number} - {self.logged_at}"


class BatteryDevice(models.Model):
    """Model representing a device containing battery(ies)."""
    
    DEVICE_TYPE_CHOICES = [
        ('MOBILE', 'Mobile Phone'),
        ('LAPTOP', 'Laptop'),
        ('DRONE', 'Drone'),
        ('VEHICLE', 'Vehicle'),
        ('INDUSTRIAL', 'Industrial Equipment'),
        ('OTHER', 'Other'),
    ]
    
    device_name = models.CharField(max_length=200)
    device_type = models.CharField(max_length=50, choices=DEVICE_TYPE_CHOICES)
    serial_number = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=200, blank=True)
    
    # Associated batteries
    batteries = models.ManyToManyField(Battery, related_name='devices')
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_checked = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['device_name']
        verbose_name = 'Battery Device'
        verbose_name_plural = 'Battery Devices'
    
    def __str__(self):
        return f"{self.device_name} ({self.serial_number})"
