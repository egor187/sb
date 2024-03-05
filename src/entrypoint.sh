#!/bin/sh

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "Trying to connect to the db..."
  sleep 1
done
echo "Connected to the db"

alembic upgrade head

exec "$@"