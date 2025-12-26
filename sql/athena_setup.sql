-- 1. Create the Database
CREATE DATABASE IF NOT EXISTS financial_data;

-- 2. Create the External Table using OpenCSV SerDe
-- This handles the double quotes and commas in company names
CREATE EXTERNAL TABLE IF NOT EXISTS financial_data.stock_prices (
  symbol STRING,
  name STRING,
  timestamp STRING,
  price_usd STRING,
  price_cad STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '\"',
  'escapeChar' = '\\'
)
LOCATION 's3://brandon-swanwick-finance-clean-1313/processed/'
TBLPROPERTIES ('skip.header.line.count'='1');

-- 3. Create a View for Visualization
-- Converts strings to proper types (Double and Timestamp) for QuickSight/BI Tools
CREATE OR REPLACE VIEW financial_data.clean_stocks AS
SELECT 
    symbol,
    name,
    CAST(from_iso8601_timestamp(timestamp) AS TIMESTAMP) as actual_timestamp,
    CAST(price_usd AS DOUBLE) as price_usd,
    CAST(price_cad AS DOUBLE) as price_cad
FROM financial_data.stock_prices;

-- Example Query for Validation
SELECT * FROM financial_data.clean_stocks 
ORDER BY actual_timestamp DESC 
LIMIT 10;