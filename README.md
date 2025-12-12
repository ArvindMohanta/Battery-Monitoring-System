# Battery Management System

A comprehensive Django-based battery management system for monitoring and tracking battery health, status, and performance metrics with an interactive analytics dashboard.

## 🎯 Overview

This is a production-ready battery management system built with Django and Django REST Framework. It provides real-time monitoring, historical data logging, automated alerting, and a beautiful interactive dashboard for battery analysis.

## ✨ Features

### Core Features
- **Interactive Dashboard**: Real-time analytics with charts, metrics, and alerts
- **Battery Monitoring**: Real-time tracking of battery charge, voltage, temperature, and health
- **Alert System**: Automatic alerts for critical conditions (low charge, overtemperature, overvoltage, etc.)
- **Data Logging**: Complete historical logging of battery readings
- **Device Management**: Manage devices containing batteries
- **REST API**: Complete RESTful API for integration
- **Admin Dashboard**: Django admin interface for system management
- **Data Export**: Export dashboard data as JSON for external analysis

### Dashboard Features
- Real-time metric cards (total batteries, active, faulty, health, charge, temperature, alerts)
- Interactive charts:
  - Battery status distribution (pie chart)
  - Health ranges (bar chart)
  - Charge level distribution (bar chart)
  - Battery types (pie chart)
  - Cycle count distribution (bar chart)
  - Alert types breakdown (bar chart)
- Detailed battery information table with visual progress bars
- Recent unresolved alerts with color-coded severity levels
- Auto-refresh every 30 seconds with manual refresh button
- Responsive design for desktop and mobile

### Alert System
- Automatic alert generation for:
  - Low charge levels
  - Overcharge conditions
  - Over temperature
  - Under voltage
  - Over current
  - Health degradation
  - Fault detection
  - Communication errors
- Multiple severity levels: INFO, WARNING, ERROR, CRITICAL
- Alert resolution tracking
- Real-time alert status updates

## 📋 Table of Contents

1. [Installation](#installation)
2. [Project Structure](#project-structure)
3. [Database Models](#database-models)
4. [API Documentation](#api-documentation)
5. [Dashboard](#dashboard)
6. [Usage Examples](#usage-examples)
7. [Configuration](#configuration)
8. [Troubleshooting](#troubleshooting)
9. [Future Enhancements](#future-enhancements)
10. [Contributing](#contributing)
11. [License](#license)

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip package manager
- Git

### Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/ArvindMohanta/Battery-Monitoring-System.git
cd Battery-Monitoring-System
```

2. **Create and activate virtual environment:**
```bash
# Linux/Mac
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser (for admin access):**
```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

6. **Load sample data (optional):**
```bash
python manage.py shell < load_sample_data.py
```

7. **Run development server:**
```bash
python manage.py runserver
```

Server will be available at: `http://localhost:8000/`

### Automated Setup Script

**Linux/Mac:**
```bash
bash setup.sh
```

**Windows:**
```bash
setup.bat
```

## 📁 Project Structure

```
Battery-Monitoring-System/
├── battery_system/              # Main project configuration
│   ├── __init__.py
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Main URL configuration
│   ├── wsgi.py                 # WSGI application
│   └── asgi.py                 # ASGI application
│
├── batteries/                   # Battery app
│   ├── __init__.py
│   ├── models.py               # Database models
│   ├── serializers.py          # REST API serializers
│   ├── views.py                # API viewsets
│   ├── dashboard_views.py      # Dashboard views
│   ├── urls.py                 # App URL configuration
│   ├── admin.py                # Django admin configuration
│   ├── apps.py                 # App configuration
│   └── migrations/             # Database migrations
│
├── templates/                   # HTML templates
│   └── batteries/
│       └── dashboard.html      # Interactive dashboard
│
├── static/                      # Static files (CSS, JS, images)
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── setup.sh                     # Linux/Mac setup script
├── setup.bat                    # Windows setup script
├── load_sample_data.py         # Sample data loader
├── .env.example                # Environment configuration template
├── .gitignore                  # Git ignore rules
├── API_DOCS.md                 # API documentation
└── README.md                   # This file
```

## 🗄️ Database Models

### Battery Model
Main model for tracking battery information and status.

**Fields:**
- `serial_number` (CharField, unique) - Unique identifier
- `battery_type` (CharField) - Type: Li-ion, NiMH, Lead-acid, etc.
- `capacity` (FloatField) - Battery capacity in mAh
- `voltage_nominal` (FloatField) - Nominal voltage in volts
- `current_charge` (FloatField) - Current charge percentage (0-100%)
- `current_voltage` (FloatField) - Current voltage in volts
- `current_temperature` (FloatField) - Temperature in Celsius
- `current_status` (CharField) - Status: CHARGING, DISCHARGING, IDLE, FAULT
- `health_percentage` (FloatField) - Battery health (0-100%)
- `cycle_count` (IntegerField) - Number of charge cycles
- `max_discharge_current` (FloatField) - Max discharge current in Amps
- `max_charge_current` (FloatField) - Max charge current in Amps
- `last_updated` (DateTimeField) - Last update timestamp
- `created_at` (DateTimeField) - Creation timestamp

**Status Values:**
- `CHARGING` - Battery is charging
- `DISCHARGING` - Battery is discharging
- `IDLE` - Battery is idle
- `FAULT` - Battery has a fault

### BatteryAlert Model
Tracks alerts and anomalies detected in batteries.

**Fields:**
- `battery` (ForeignKey) - Reference to Battery
- `alert_type` (CharField) - Type of alert
- `alert_level` (CharField) - Severity: INFO, WARNING, ERROR, CRITICAL
- `message` (TextField) - Alert message
- `is_resolved` (BooleanField) - Resolution status
- `created_at` (DateTimeField) - Creation timestamp
- `resolved_at` (DateTimeField, nullable) - Resolution timestamp

**Alert Types:**
- `LOW_CHARGE` - Battery charge is low
- `OVERCHARGE` - Battery is overcharged
- `OVER_TEMPERATURE` - Temperature too high
- `UNDER_VOLTAGE` - Voltage too low
- `OVER_CURRENT` - Current too high
- `HEALTH_DEGRADATION` - Health has degraded
- `FAULT` - Fault detected
- `COMMUNICATION_ERROR` - Communication error

**Alert Levels:**
- `INFO` - Information
- `WARNING` - Warning
- `ERROR` - Error
- `CRITICAL` - Critical

### BatteryLog Model
Historical logging of battery readings.

**Fields:**
- `battery` (ForeignKey) - Reference to Battery
- `charge_percentage` (FloatField) - Charge at logging time
- `voltage` (FloatField) - Voltage at logging time
- `temperature` (FloatField) - Temperature at logging time
- `current` (FloatField) - Current (positive: charging, negative: discharging)
- `status` (CharField) - Battery status
- `logged_at` (DateTimeField) - Logging timestamp

**Indexes:**
- Composite index on (battery, -logged_at) for efficient querying

### BatteryDevice Model
Manages devices containing batteries.

**Fields:**
- `device_name` (CharField) - Device name
- `device_type` (CharField) - Type: MOBILE, LAPTOP, DRONE, VEHICLE, INDUSTRIAL, OTHER
- `serial_number` (CharField, unique) - Device serial number
- `location` (CharField) - Device location
- `batteries` (ManyToManyField) - Associated batteries
- `is_active` (BooleanField) - Active status
- `created_at` (DateTimeField) - Creation timestamp
- `last_checked` (DateTimeField, nullable) - Last check time

## 📡 API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Authentication
Currently supports Django's built-in authentication. For production, implement JWT tokens.

### Response Format
All responses are in JSON format with standard HTTP status codes.

### Pagination
- Default page size: 20 items
- Pagination via query parameter: `?page=1`

### Filtering & Search
- Search via query parameter: `?search=term`
- Order via query parameter: `?ordering=field`

---

## 🎨 Dashboard Endpoints

### Dashboard UI
```
GET /dashboard/
```
Returns the interactive HTML dashboard with real-time metrics and charts.

**Access:** http://localhost:8000/dashboard/

### Dashboard Statistics (JSON)
```
GET /api/dashboard/stats/
```

**Response:**
```json
{
  "batteries": {
    "total": 3,
    "active": 2,
    "faulty": 0
  },
  "health": {
    "average": 94.33,
    "low_count": 0
  },
  "charge": {
    "average": 75.0
  },
  "temperature": {
    "average": 28.33
  },
  "alerts": {
    "total": 1,
    "unresolved": 1,
    "critical": 0
  },
  "devices": {
    "total": 1,
    "active": 1
  }
}
```

### Chart Data
```
GET /api/dashboard/chart-data/
```

Returns data for all dashboard charts including status distribution, health ranges, charge levels, etc.

### Battery Details
```
GET /api/dashboard/battery-details/
```

Returns detailed information for all batteries.

### Alert Summary
```
GET /api/dashboard/alerts/
```

Returns alert type breakdown, levels breakdown, and recent unresolved alerts.

### Battery Trends
```
GET /api/dashboard/trend/?battery_id={id}
```

Returns historical trend data for a specific battery or all batteries.

**Query Parameters:**
- `battery_id` (optional) - Battery ID to get specific trends

### Dashboard Export
```
GET /api/dashboard/export/
```

Exports complete dashboard data including timestamp, stats, charts, batteries, and alerts.

---

## 🔋 Battery API

### List Batteries
```
GET /api/batteries/
```

**Query Parameters:**
- `search` - Search by serial number or type
- `ordering` - Order by: current_charge, health_percentage, created_at
- `page` - Page number

**Example:**
```bash
curl http://localhost:8000/api/batteries/?search=Li-ion&ordering=-health_percentage&page=1
```

### Get Battery
```
GET /api/batteries/{id}/
```

### Create Battery
```
POST /api/batteries/
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

### Update Battery
```
PUT /api/batteries/{id}/
Content-Type: application/json

{
  "current_charge": 85,
  "health_percentage": 98
}
```

### Delete Battery
```
DELETE /api/batteries/{id}/
```

### Update Battery Status
```
POST /api/batteries/{id}/update_status/
Content-Type: application/json

{
  "current_charge": 85,
  "current_voltage": 3.6,
  "current_temperature": 28,
  "current_status": "DISCHARGING",
  "current": -2.5
}
```

This endpoint also logs the reading and checks for alerts.

### Get Battery Health Report
```
GET /api/batteries/{id}/health_report/
```

Returns comprehensive health report including battery details, recent alerts, recent readings, and average temperature.

### Get Low Health Batteries
```
GET /api/batteries/low_health_batteries/?threshold=80
```

**Query Parameters:**
- `threshold` - Health threshold (default: 80)

### Get Critical Status Batteries
```
GET /api/batteries/critical_status_batteries/
```

Returns all batteries with FAULT status.

---

## 🚨 Alert API

### List Alerts
```
GET /api/alerts/
```

### Create Alert
```
POST /api/alerts/
Content-Type: application/json

{
  "battery": 1,
  "alert_type": "LOW_CHARGE",
  "alert_level": "WARNING",
  "message": "Battery charge is low"
}
```

### Get Alert
```
GET /api/alerts/{id}/
```

### Update Alert
```
PUT /api/alerts/{id}/
```

### Delete Alert
```
DELETE /api/alerts/{id}/
```

### Resolve Alert
```
POST /api/alerts/{id}/resolve/
```

### Get Unresolved Alerts
```
GET /api/alerts/unresolved/
```

---

## 📊 Log API

### List Logs
```
GET /api/logs/
```

**Query Parameters:**
- `search` - Search by battery serial number
- `ordering` - Order by logged_at
- `page` - Page number

### Get Log
```
GET /api/logs/{id}/
```

Note: Log endpoints are read-only. Logs are created via battery status updates.

---

## 🖥️ Device API

### List Devices
```
GET /api/devices/
```

### Create Device
```
POST /api/devices/
Content-Type: application/json

{
  "device_name": "Laptop - MacBook Pro",
  "device_type": "LAPTOP",
  "serial_number": "DEVICE-002",
  "location": "Office A",
  "batteries": [1, 2]
}
```

### Get Device
```
GET /api/devices/{id}/
```

### Update Device
```
PUT /api/devices/{id}/
```

### Delete Device
```
DELETE /api/devices/{id}/
```

### Get Device Battery Status
```
GET /api/devices/{id}/battery_status/
```

Returns device details with all associated batteries and their current status.

---

## 💻 Usage Examples

### Python Client Example
```python
import requests
import json

BASE_URL = 'http://localhost:8000/api'

# Get all batteries
response = requests.get(f'{BASE_URL}/batteries/')
batteries = response.json()
print(f"Total batteries: {len(batteries['results'])}")

# Create a new battery
battery_data = {
    'serial_number': 'BAT-NEW-001',
    'battery_type': 'Li-ion',
    'capacity': 5000,
    'voltage_nominal': 3.7,
    'current_charge': 100,
    'current_voltage': 3.7,
    'current_temperature': 25,
    'current_status': 'IDLE',
    'health_percentage': 100,
    'cycle_count': 0,
    'max_discharge_current': 10,
    'max_charge_current': 5
}

response = requests.post(f'{BASE_URL}/batteries/', json=battery_data)
if response.status_code == 201:
    new_battery = response.json()
    print(f"Created battery: {new_battery['serial_number']}")
    battery_id = new_battery['id']
    
    # Update battery status
    update_data = {
        'current_charge': 75,
        'current_voltage': 3.5,
        'current_temperature': 30,
        'current_status': 'DISCHARGING',
        'current': -2.5
    }
    
    response = requests.post(
        f'{BASE_URL}/batteries/{battery_id}/update_status/',
        json=update_data
    )
    print(f"Updated battery status: {response.status_code}")
    
    # Get health report
    response = requests.get(f'{BASE_URL}/batteries/{battery_id}/health_report/')
    health_report = response.json()
    print(f"Health: {health_report['battery']['health_percentage']}%")

# Get unresolved alerts
response = requests.get(f'{BASE_URL}/alerts/unresolved/')
alerts = response.json()
print(f"Unresolved alerts: {len(alerts['results'])}")

# Get dashboard statistics
response = requests.get(f'{BASE_URL}/dashboard/stats/')
stats = response.json()
print(f"Total batteries: {stats['batteries']['total']}")
print(f"Average health: {stats['health']['average']}%")
```

### cURL Examples

**Get Dashboard Stats:**
```bash
curl http://localhost:8000/api/dashboard/stats/
```

**Create Battery:**
```bash
curl -X POST http://localhost:8000/api/batteries/ \
  -H "Content-Type: application/json" \
  -d '{
    "serial_number": "BAT-001",
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
  }'
```

**Update Battery Status:**
```bash
curl -X POST http://localhost:8000/api/batteries/1/update_status/ \
  -H "Content-Type: application/json" \
  -d '{
    "current_charge": 85,
    "current_voltage": 3.6,
    "current_temperature": 28,
    "current_status": "DISCHARGING",
    "current": -2.5
  }'
```

**Get Unresolved Alerts:**
```bash
curl http://localhost:8000/api/alerts/unresolved/
```

---

## ⚙️ Configuration

### Environment Variables
Create a `.env` file based on `.env.example`:

```
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Database Configuration

**SQLite (Default):**
Already configured in settings.py

**PostgreSQL:**
Update settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'battery_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Install PostgreSQL driver:
```bash
pip install psycopg2-binary
```

### Static Files
Collect static files for production:
```bash
python manage.py collectstatic
```

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Linux/Mac - Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
python manage.py runserver 8001
```

### Database Issues
```bash
# Reset database
rm db.sqlite3

# Recreate migrations
python manage.py makemigrations
python manage.py migrate

# Create new superuser
python manage.py createsuperuser
```

### Module Not Found Error
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Templates Not Found
```bash
# Ensure templates directory exists
mkdir -p templates/batteries

# Check TEMPLATES setting in settings.py
```

### Static Files 404
```bash
# Ensure static directory exists
mkdir -p static

# For development
python manage.py runserver

# For production
python manage.py collectstatic --noinput
```

### Database Locked Error (SQLite)
```bash
# Close all connections and restart server
# Ensure only one runserver instance is running
```

---

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False` in settings.py
- [ ] Set strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use production database (PostgreSQL recommended)
- [ ] Set up HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Set up email backend
- [ ] Use Gunicorn/uWSGI
- [ ] Set up static file serving (Nginx/Apache)
- [ ] Configure logging
- [ ] Set up database backups

### Using Gunicorn
```bash
pip install gunicorn
gunicorn battery_system.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker (Optional)
```dockerfile
FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "battery_system.wsgi:application", "--bind", "0.0.0.0:8000"]
```

---

## 📈 Future Enhancements

- [ ] WebSocket support for real-time updates
- [ ] Machine learning for battery health prediction
- [ ] IoT device integration
- [ ] Advanced analytics and reporting
- [ ] Email/SMS notifications
- [ ] Mobile app (React Native/Flutter)
- [ ] Data visualization improvements
- [ ] User authentication system
- [ ] Role-based access control
- [ ] Data backup and recovery
- [ ] Performance optimization with caching
- [ ] API rate limiting
- [ ] Swagger API documentation
- [ ] GraphQL API
- [ ] Battery lifecycle analysis

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 conventions
- Use meaningful variable names
- Add docstrings to functions
- Write unit tests for new features

---

## 📝 License

This project is open source and available under the MIT License.

---

## 📞 Support

For issues, questions, or suggestions:
- Create an issue in the repository
- Check existing documentation
- Review API_DOCS.md for API details

---

## 🙏 Acknowledgments

- Django Framework
- Django REST Framework
- Chart.js for visualizations
- Bootstrap for responsive design

---

## 📊 System Requirements

- Python 3.8+
- pip
- 100MB disk space minimum
- Modern web browser (Chrome, Firefox, Safari, Edge)

---

## 📝 Version History

**v1.0.0** (December 2025)
- Initial release
- Core battery monitoring
- REST API
- Interactive dashboard
- Alert system
- Admin interface
- Sample data loader

---

**Last Updated:** December 12, 2025

For the latest updates, visit the [GitHub Repository](https://github.com/ArvindMohanta/Battery-Monitoring-System)
