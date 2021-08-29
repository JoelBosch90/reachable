#!/usr/bin/env python
"""
Manage

Django's command-line utility for administrative tasks.
"""


# Import dependencies.
import os
import sys


"""
Main

This is the main process that is called when this file is opened explicitly.
"""
def main():

    # Run administrative tasks.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

    # Try importing Django.
    try:
        from django.core.management import execute_from_command_line
        from django.core.management.commands.runserver import Command as runserver
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Change the default port for running the server.
    runserver.default_port = "3000"

    # Run the server.
    execute_from_command_line(sys.argv)


# Check if this file was opened explicitly to execute and only then run the main
# function. This way, we can prevent the runtime execution of this program when
# it is imported into a different file.
if __name__ == '__main__':
    main()
