#!/bin/sh
set -e

echo "Esperando MySQL en ${DB_HOST:-mysql}:${DB_PORT:-3306}..."

until nc -z "${DB_HOST:-mysql}" "${DB_PORT:-3306}"; do
  echo "MySQL no disponible aún..."
  sleep 3
done

echo "MySQL disponible, iniciando API de despachos..."
exec java -jar app.jar
