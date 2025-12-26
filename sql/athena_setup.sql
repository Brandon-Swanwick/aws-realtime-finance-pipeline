-- 1. Create the Database
CREATE DATABASE IF NOT EXISTS financial_data;

-- 2. Updated Table Schema to include pct_change
CREATE EXTERNAL TABLE IF NOT EXISTS financial_data.stock_prices (
  symbol STRING,
  name STRING,
  timestamp STRING,
  price_usd STRING,
  price_cad STRING,
  pct_change STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '\"',
  'escapeChar' = '\\'
)
LOCATION 's3://brandon-swanwick-finance-clean-1313/processed/'
TBLPROPERTIES ('skip.header.line.count'='1');

-- 3. Updated View with pct_change casted to DOUBLE
CREATE OR REPLACE VIEW financial_data.clean_stocks AS
SELECT 
    symbol,
    name,
    CAST(from_iso8601_timestamp(timestamp) AS TIMESTAMP) as actual_timestamp,
    CAST(price_usd AS DOUBLE) as price_usd,
    CAST(price_cad AS DOUBLE) as price_cad,
    CAST(pct_change AS DOUBLE) as pct_change
FROM financial_data.stock_prices;