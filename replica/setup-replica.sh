#!/bin/bash

set -e

echo "Waiting for primary..."

until pg_isready -h primary -p 5432 -U postgres
do
    sleep 2
done

rm -rf /var/lib/postgresql/data/*

PGPASSWORD=RANGEROVER pg_basebackup \
    -h primary \
    -D /var/lib/postgresql/data \
    -U replicator \
    -Fp \
    -Xs \
    -P \
    -R

echo "Base backup completed."

exec docker-entrypoint.sh postgres