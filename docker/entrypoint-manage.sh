#!/bin/bash
set -e

python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate --noinput

echo "from accounts.models import User;
User.objects.filter(email='$DJANGO_SUPERUSER_EMAIL').delete();
User.objects.create_superuser('$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')" | python manage.py shell

#exec "$@"
#exec tail -f /dev/null
