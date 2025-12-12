"""
Sample data loader for Battery Management System.
Run with: python manage.py shell < load_sample_data.py
"""

from batteries.models import Battery, BatteryDevice, BatteryAlert, BatteryLog
from django.utils import timezone

# Create sample batteries
batteries_data = [
    {
        'serial_number': 'BAT-001',
        'battery_type': 'Li-ion',
        'capacity': 5000,
        'voltage_nominal': 3.7,
        'current_charge': 85,
        'current_voltage': 3.65,
        'current_temperature': 25,
        'current_status': 'DISCHARGING',
        'health_percentage': 95,
        'cycle_count': 150,
        'max_discharge_current': 10,
        'max_charge_current': 5
    },
    {
        'serial_number': 'BAT-002',
        'battery_type': 'Li-ion',
        'capacity': 4000,
        'voltage_nominal': 3.7,
        'current_charge': 45,
        'current_voltage': 3.4,
        'current_temperature': 32,
        'current_status': 'CHARGING',
        'health_percentage': 88,
        'cycle_count': 320,
        'max_discharge_current': 8,
        'max_charge_current': 4
    },
    {
        'serial_number': 'BAT-003',
        'battery_type': 'NiMH',
        'capacity': 2500,
        'voltage_nominal': 1.2,
        'current_charge': 100,
        'current_voltage': 1.2,
        'current_temperature': 22,
        'current_status': 'IDLE',
        'health_percentage': 100,
        'cycle_count': 50,
        'max_discharge_current': 5,
        'max_charge_current': 2.5
    }
]

print("Creating sample batteries...")
batteries = []
for data in batteries_data:
    battery, created = Battery.objects.get_or_create(
        serial_number=data['serial_number'],
        defaults=data
    )
    batteries.append(battery)
    if created:
        print(f"  Created: {battery.serial_number}")
    else:
        print(f"  Already exists: {battery.serial_number}")

# Create sample device
print("\nCreating sample device...")
device, created = BatteryDevice.objects.get_or_create(
    serial_number='DEVICE-001',
    defaults={
        'device_name': 'Mobile Phone - iPhone 14',
        'device_type': 'MOBILE',
        'location': 'Warehouse 1'
    }
)
device.batteries.set(batteries[:2])
if created:
    print(f"  Created: {device.device_name}")
else:
    print(f"  Already exists: {device.device_name}")

# Create sample logs
print("\nCreating sample battery logs...")
for battery in batteries:
    BatteryLog.objects.get_or_create(
        battery=battery,
        logged_at=timezone.now(),
        defaults={
            'charge_percentage': battery.current_charge,
            'voltage': battery.current_voltage,
            'temperature': battery.current_temperature,
            'current': -2.5 if battery.current_status == 'DISCHARGING' else 2.0 if battery.current_status == 'CHARGING' else 0,
            'status': battery.current_status
        }
    )
print(f"  Created logs for {len(batteries)} batteries")

# Create sample alert
print("\nCreating sample alert...")
alert, created = BatteryAlert.objects.get_or_create(
    battery=batteries[1],
    alert_type='OVER_TEMPERATURE',
    defaults={
        'alert_level': 'WARNING',
        'message': 'Battery temperature is elevated',
        'is_resolved': False
    }
)
if created:
    print(f"  Created alert: {alert.alert_type}")
else:
    print(f"  Alert already exists")

print("\nSample data loaded successfully!")
