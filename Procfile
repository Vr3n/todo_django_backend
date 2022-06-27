web: gunicorn todo_backend.wsgi
release: sh -c "python manage.py collectstatic && python manage.py makemigrations users todos && python manage.py migrate"
