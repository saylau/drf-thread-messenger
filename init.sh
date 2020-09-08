#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER aero_chat WITH PASSWORD 'aero_chat';
    GRANT ALL PRIVILEGES ON DATABASE aero_chat TO aero_chat;
EOSQL