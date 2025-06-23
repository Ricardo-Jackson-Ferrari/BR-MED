#!/bin/sh
set -e

echo "Aguardando o banco de dados estar disponível em $DB_HOST:$DB_PORT..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "Banco de dados disponível, aplicando migrações..."

python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "Iniciando Gunicorn..."

exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
