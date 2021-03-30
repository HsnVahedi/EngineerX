rm manage.py && mv manage.production.py manage.py
rm engineerx/wsgi.py && mv engineerx/wsgi.production.py engineerx/wsgi.py

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

gunicorn engineerx.wsgi:application