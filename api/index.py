import os
import sys
from pathlib import Path

# Make the Django project (where manage.py lives) importable
PROJECT_DIR = Path(__file__).resolve().parent.parent / "django" / "1hr" / "workspace" / "myapp"
sys.path.insert(0, str(PROJECT_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myapp.settings")

from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()

# Auto-create/update database tables on cold start (only when a DATABASE_URL is set)
if os.environ.get("DATABASE_URL"):
    try:
        from django.core.management import call_command
        call_command("migrate", interactive=False, verbosity=0)
    except Exception as exc:  # don't take the site down if migrate fails
        print("migrate failed:", exc)

# Vercel looks for a WSGI callable named `app`
app = application
