web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && python manage.py create_superuser_if_needed && gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT --log-file -
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput && python manage.py create_superuser_if_needed

