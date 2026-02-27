#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$SCRIPT_DIR/../data"
COMPOSE_FILE="$SCRIPT_DIR/../docker-compose.yml"

# ---------- CONFIG ----------
DB_NAME="appdb"
DB_USER="appuser"
CSV_PATH="$DATA_DIR/ChocolateSales.csv"
TABLE_NAME="chocolate_sales"
STAGING_TABLE="chocolate_sales_staging"
# ----------------------------

# copy csv file into docker container:file_path
docker cp "$CSV_PATH" infrastructure-postgres-1:/var/lib/postgresql/data

DOCKER_CSV_PATH="/var/lib/postgresql/data/ChocolateSales.csv"

docker compose -f "$COMPOSE_FILE" exec -T postgres psql -U "$DB_USER" -d "$DB_NAME" <<EOF

-- Drop tables if they exist
DROP TABLE IF EXISTS $TABLE_NAME;
DROP TABLE IF EXISTS $STAGING_TABLE;

-- 1. Staging table (all text, mirrors CSV)
CREATE TABLE $STAGING_TABLE (
    sales_person TEXT,
    country TEXT,
    product TEXT,
    sale_date TEXT,
    amount TEXT,
    boxes_shipped TEXT
);

-- 2. Load raw CSV data
COPY $STAGING_TABLE
FROM '$DOCKER_CSV_PATH'
DELIMITER ','
CSV HEADER;

-- 3. Final typed table
CREATE TABLE $TABLE_NAME (
    id SERIAL PRIMARY KEY,
    sales_person TEXT,
    country TEXT,
    product TEXT,
    sale_date DATE,
    amount NUMERIC(12,2),
    boxes_shipped INTEGER
);

-- 4. Transform and insert clean data
INSERT INTO $TABLE_NAME (
    sales_person,
    country,
    product,
    sale_date,
    amount,
    boxes_shipped
)
SELECT
    sales_person,
    country,
    product,
    to_date(sale_date, 'DD/MM/YYYY'),
    REPLACE(REPLACE(amount, '$', ''), ',', '')::NUMERIC(12,2),
    boxes_shipped::INTEGER
FROM $STAGING_TABLE;

-- 5. Drop staging table
DROP TABLE $STAGING_TABLE;

EOF

echo "Chocolate sales data successfully loaded into table: $TABLE_NAME"
