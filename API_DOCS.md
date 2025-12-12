# Django Battery Management System

## Welcome

Welcome to Battery Management System

### Documentation

- Dashboard: `/dashboard/`
- Admin: `/admin/`
- API root: `/api/`

#### API Endpoints

- Batteries: `/api/batteries/`
- Alerts: `/api/alerts/`
- Logs: `/api/logs/`
- Devices: `/api/devices/`
- Dashboard stats: `/api/dashboard/stats/`
- Chart data: `/api/dashboard/chart-data/`
- Battery details: `/api/dashboard/battery-details/`
- Alerts summary: `/api/dashboard/alerts/`
- Battery trends: `/api/dashboard/trend/`

### Features

- Real-time battery monitoring
- Interactive analytics dashboard
- Alert management
- Historical data logging
- Device management
- Complete REST API

## API Documentation
## Quick Start

### 1. Setup Project
```bash
# Linux/Mac
bash setup.sh

# Windows
setup.bat
```

### 2. Run Development Server
```bash
python manage.py runserver
```

### 3. Access Dashboard
- Admin: http://localhost:8000/admin/
- API: http://localhost:8000/api/

## API Documentation

### Authentication
Currently uses Django's built-in authentication. For production, consider implementing JWT tokens.

### Base URL
`http://localhost:8000/api/`

### Response Format
All responses are in JSON format.

## Endpoints

### Batteries

#### List Batteries
```
GET /batteries/
```

Query Parameters:
- `search` - Search by serial number or battery type
- `ordering` - Order by: current_charge, health_percentage, created_at
- `page` - Page number (default: 1)

Example:
```bash
curl http://localhost:8000/api/batteries/?search=Li-ion&ordering=-current_charge
```

#### Get Battery Details
```
GET /batteries/{id}/
```

#### Create Battery
```
POST /batteries/
Content-Type: application/json

{
  "serial_number": "BAT-004",
  "battery_type": "Li-ion",
  "capacity": 5000,
  "voltage_nominal": 3.7,
  "current_charge": 100,
  "current_voltage": 3.7,
  "current_temperature": 25,
  "current_status": "IDLE",
  "health_percentage": 100,
  "cycle_count": 0,
  "max_discharge_current": 10,
  "max_charge_current": 5
}
```

#### Update Battery Status
```
POST /batteries/{id}/update_status/
Content-Type: application/json

{
  "current_charge": 85,
  "current_voltage": 3.6,
  "current_temperature": 28,
  "current_status": "DISCHARGING",
  "current": -2.5
}
```

#### Get Battery Health Report
```
GET /batteries/{id}/health_report/
```

Response includes:
- Battery details
- Recent alerts
- Recent readings
- Average temperature

#### Get Low Health Batteries
```
GET /batteries/low_health_batteries/?threshold=80
```

#### Get Critical Status Batteries
```
GET /batteries/critical_status_batteries/
```

### Alerts

#### List Alerts
```
GET /alerts/
```

Query Parameters:
- `search` - Search by alert type or battery serial number
- `ordering` - Order by: created_at, alert_level

#### Get Unresolved Alerts
```
GET /alerts/unresolved/
```

#### Resolve Alert
```
POST /alerts/{id}/resolve/
```

### Logs

#### List Logs
```
GET /logs/
```

Query Parameters:
- `search` - Search by battery serial number
- `ordering` - Order by: logged_at

### Devices

#### List Devices
```
GET /devices/
```

#### Get Device Battery Status
```
GET /devices/{id}/battery_status/
```

Returns all batteries associated with the device.

#### Create Device
```
POST /devices/
Content-Type: application/json

{
  "device_name": "Laptop - MacBook Pro",
  "device_type": "LAPTOP",
  "serial_number": "DEVICE-002",
  "location": "Office A",
  "batteries": [1, 2]
}
```

## Status Codes

- `200` - OK
- `201` - Created
- `204` - No Content
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `500` - Internal Server Error

## Error Response Format

```json
{
  "error": "Error message",
  "details": {
    "field": ["error message"]
  }
}
```

## Rate Limiting

Not currently implemented. Consider adding for production:
```python
# Add to settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}
```

## Pagination

Default page size: 20 items

Example:
```bash
curl http://localhost:8000/api/batteries/?page=2
```

## Filtering

### Battery Status
- CHARGING - Battery is charging
- DISCHARGING - Battery is discharging
- IDLE - Battery is idle
- FAULT - Battery has a fault

### Alert Levels
- INFO - Information level
- WARNING - Warning level
- ERROR - Error level
- CRITICAL - Critical level

### Alert Types
- LOW_CHARGE - Battery charge is low
- OVERCHARGE - Battery is overcharged
- OVER_TEMPERATURE - Battery temperature is too high
- UNDER_VOLTAGE - Battery voltage is too low
- OVER_CURRENT - Battery current is too high
- HEALTH_DEGRADATION - Battery health has degraded
- FAULT - Fault detected
- COMMUNICATION_ERROR - Communication error

## Sample Python Client

```python
import requests

BASE_URL = 'http://localhost:8000/api'

# Get all batteries
response = requests.get(f'{BASE_URL}/batteries/')
batteries = response.json()

# Create a new battery
battery_data = {
    'serial_number': 'BAT-NEW',
    'battery_type': 'Li-ion',
    # ... other fields
}
response = requests.post(f'{BASE_URL}/batteries/', json=battery_data)
new_battery = response.json()

# Update battery status
update_data = {
    'current_charge': 75,
    'current_voltage': 3.5,
    'current_temperature': 30,
    'current_status': 'DISCHARGING'
}
response = requests.post(
    f'{BASE_URL}/batteries/{new_battery["id"]}/update_status/',
    json=update_data
)
```

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
python manage.py runserver 8001
```

### Database Issues
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Module Not Found
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

## Support

For issues and questions, please refer to the main README.md or create an issue in the repository.
