web: python manage.py collectstatic --noinput && python manage.py migrate && gunicorn config.wsgi --timeout 180 --log-file -
