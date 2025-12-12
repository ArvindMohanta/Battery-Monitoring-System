@echo off
REM Battery Management System - Quick Setup Script for Windows

echo ===================================
echo Battery Management System Setup
echo ===================================

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Run migrations
echo Running migrations...
python manage.py makemigrations
python manage.py migrate

REM Create superuser
echo.
echo ===================================
echo Creating superuser account
echo ===================================
python manage.py createsuperuser

REM Display completion message
echo.
echo ===================================
echo Setup Complete!
echo ===================================
echo.
echo To start the development server, run:
echo   venv\Scripts\activate.bat
echo   python manage.py runserver
echo.
echo Django Admin: http://localhost:8000/admin/
echo API: http://localhost:8000/api/
