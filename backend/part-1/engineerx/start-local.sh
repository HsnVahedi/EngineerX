rm manage.py && mv manage.local.py manage.py
rm engineerx/wsgi.py && mv engineerx/wsgi.local.py engineerx/wsgi.py
mv -vn downloads/ media/downloads/
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn engineerx.wsgi:application