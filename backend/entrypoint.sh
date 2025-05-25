#!/bin/bash

set -e

echo "⏳ Waiting for database at $POSTGRES_HOST..."
until nc -z "$POSTGRES_HOST" 5432; do
  sleep 1
done
echo "✅ PostgreSQL is ready!"

echo "🛠 Running Django migrations..."
python manage.py migrate --noinput

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

if [ "$CREATE_SUPERUSER" = "true" ]; then
  echo "👤 Creating superuser..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="${DJANGO_SU_NAME}").exists():
    User.objects.create_superuser(
        username="${DJANGO_SU_NAME}",
        email="${DJANGO_SU_EMAIL}",
        password="${DJANGO_SU_PASSWORD}"
    )
EOF
echo "✅ superuser "$DJANGO_SU_NAME" created... successfully"
fi

echo "🚀 Completed entrypoint task..."

if [ "$ENVIRONMENT" = "dev" ]; then
  echo "🚀 Starting debug server..."
  python manage.py runserver 0.0.0.0:8000
else
  echo "🚀 Starting production server..."
  gunicorn backend.wsgi:application --bind 0.0.0.0:8000
fi

exec "$@"