#!/bin/sh
set -e

echo "Esperando MySQL en ${DB_HOST:-mysql}:${DB_PORT:-3306}..."

MAX_ATTEMPTS=60
attempt=0
until nc -z "${DB_HOST:-mysql}" "${DB_PORT:-3306}"; do
  attempt=$((attempt + 1))
  if [ "${attempt}" -ge "${MAX_ATTEMPTS}" ]; then
    echo "Timeout: MySQL no respondio en $((MAX_ATTEMPTS * 3))s"
    exit 1
  fi
  echo "MySQL no disponible aún (${attempt}/${MAX_ATTEMPTS})..."
  sleep 3
done

echo "MySQL disponible, iniciando API de ventas..."
exec java -jar app.jar
