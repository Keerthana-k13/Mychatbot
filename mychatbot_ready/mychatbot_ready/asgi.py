# asgi.py placeholder
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mychatbot_ready.settings')

application = get_asgi_application()