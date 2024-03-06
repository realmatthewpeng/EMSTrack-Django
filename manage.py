#!/usr/bin/env python
import os
import sys

# ONE VEHICLE, MULTIPLE ORGANIZATIONS EACH VEHICLE, ONE FOREIGN KEY TO ITS ORGANIZATIONS 
# ADD A FIELD TO VEHICLES CALLED "organization" THAT STORES THE FOREIGN KEY
# ADD A MIGRATION TO UPDATE DATABASE (ALL EXISTING VEHICLES HAVE TO POINT TO AN ORG, BUT THESE VEHICLES WERE CREATED BEFORE ORGS EXISTED BUT THEY HAVE TO POINT AT SOMETHING.) 
# BEFORE TESTING, MAKE SURE TO CREATE A NEW AMBULANCE

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emstrack.settings")
    if len(sys.argv) > 1 and (sys.argv[1] == 'flush' or
                              sys.argv[1] == 'loaddata' or
                              sys.argv[1] == 'bootstrap' or
                              sys.argv[1] == 'mqttseed'):
        os.environ.setdefault("DJANGO_ENABLE_MQTT_PUBLISH", "False")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
