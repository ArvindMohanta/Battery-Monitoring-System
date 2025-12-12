#!/bin/bash

# Battery Management System - Quick Setup Script

echo "==================================="
echo "Battery Management System Setup"
echo "==================================="

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo ""
echo "==================================="
echo "Creating superuser account"
echo "==================================="
python manage.py createsuperuser

# Display completion message
echo ""
echo "==================================="
echo "Setup Complete!"
echo "==================================="
echo ""
echo "To start the development server, run:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Django Admin: http://localhost:8000/admin/"
echo "API: http://localhost:8000/api/"
