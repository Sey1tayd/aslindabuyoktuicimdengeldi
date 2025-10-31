web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && python manage.py create_superuser_if_needed && gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT --timeout 300 --limit-request-line 8190 --limit-request-fields 32768 --limit-request-field_size 1048576 --worker-class sync --workers 2 --log-file -
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput && python manage.py create_superuser_if_needed

