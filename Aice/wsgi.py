# wsgi.py

import os
import sys

# Add the path to your project
path = '/path/to/your/project'
if path not in sys.path:
    sys.path.append(path)

# Set the DJANGO_SETTINGS_MODULE
os.environ['DJANGO_SETTINGS_MODULE'] = 'yourproject.settings'

# Get the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
