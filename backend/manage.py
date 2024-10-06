#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def check_db_connection():
    """Check database connection and print the status."""
    try:
        from django.db import connections
        from django.db.utils import OperationalError
        # Test the default database connection
        connection = connections['default']
        connection.ensure_connection()
        print("Database connection successful!")
    except OperationalError:
        print("Database connection failed!")


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FoodApp.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Check the database connection before running the management command
    check_db_connection()

    # Run the Django management command
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
