from django.apps import AppConfig
import os
import logging

from django.contrib.auth import get_user_model
from django.db import connection
from django.db.utils import OperationalError, ProgrammingError


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """Best-effort superuser creation at startup using env vars.

        This is a safety net when the Procfile release step is skipped by the host.
        It will only create a superuser if all DJANGO_SUPERUSER_* vars are set and
        the user does not already exist. It is resilient to missing tables during
        initial migration phase and will silently no-op in that case.
        """
        logger = logging.getLogger(__name__)

        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        # If variables are not fully provided, skip.
        if not username or not email or not password:
            return

        # Ensure auth tables exist before querying
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 1 FROM information_schema.tables
                    WHERE table_name IN ('auth_user', 'accounts_user')
                    LIMIT 1
                """)
                has_user_table = cursor.fetchone() is not None
        except Exception:
            # Database not ready yet; skip silently
            return

        if not has_user_table:
            return

        try:
            User = get_user_model()
            if User.objects.filter(username=username).exists():
                return
            User.objects.create_superuser(username=username, email=email, password=password)
            logger.info("Startup: superuser '%s' created.", username)
        except (OperationalError, ProgrammingError):
            # Happens if migrations not yet applied
            return
        except Exception as exc:
            # Do not crash app on startup due to superuser creation
            logger.warning("Startup: failed to ensure superuser: %s", exc)
