#!/bin/bash
# Development script for Sky Food Corner

# Activate virtual environment
source venv/bin/activate

# Check if command is provided
if [ $# -eq 0 ]; then
    echo "Usage: ./dev.sh [command]"
    echo "Commands:"
    echo "  run        - Start development server"
    echo "  migrate    - Run database migrations"
    echo "  createsuperuser - Create admin user"
    echo "  build-css  - Build Tailwind CSS"
    echo "  watch-css  - Watch and rebuild CSS"
    echo "  collectstatic - Collect static files"
    exit 1
fi

case $1 in
    "run")
        echo "Starting development server..."
        python manage.py runserver
        ;;
    "migrate")
        echo "Running migrations..."
        python manage.py migrate
        ;;
    "createsuperuser")
        echo "Creating superuser..."
        python manage.py createsuperuser
        ;;
    "build-css")
        echo "Building CSS..."
        npm run build-css
        ;;
    "watch-css")
        echo "Watching CSS files..."
        npm run watch-css
        ;;
    "collectstatic")
        echo "Collecting static files..."
        python manage.py collectstatic --noinput
        ;;
    *)
        echo "Unknown command: $1"
        echo "Available commands: run, migrate, createsuperuser, build-css, watch-css, collectstatic"
        ;;
esac