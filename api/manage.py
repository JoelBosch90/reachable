#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.
"""
import os
import sys
from django.core.management.commands.runserver import Command as runserver


def main():

    # Change the default port for running the server.
    runserver.default_port = "3000"

    # Run administrative tasks.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


# Check if this file was opened explicitly to execute and only then run the main
# function. This way, we can prevent the runtime execution of this program when
# it is imported into a different file.
if __name__ == '__main__':
    main()
