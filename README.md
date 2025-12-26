Real-Time Financial Data Pipeline (AWS Serverless)
==================================================

An automated, event-driven ETL (Extract, Transform, Load) pipeline built on AWS to ingest, process, and query real-time stock market data. This project demonstrates the ability to build scalable cloud infrastructure that handles raw API data and transforms it into analytics-ready SQL tables.

🏗️ Architecture & Data Flow
----------------------------

1.  **Ingestion (The Producer):** An AWS Lambda function triggered every 5 minutes by Amazon EventBridge. It fetches real-time stock quotes (Price, Change, and Percent Change) via the Financial Modeling Prep API.
    
2.  **Raw Storage (Bronze):**  Data is stored in its original JSON/CSV format in the raw-data-bucket for auditing and historical replay.
    
3.  **Transformation (The Consumer):** An S3-triggered Lambda function detects the new file, cleans the headers, and performs data cleaning using Python's csv and urllib modules.
    
4.  **Analytics Layer (Silver):** The processed data is saved to the clean-data-bucket in a flat CSV format optimized for **Amazon Athena**.
    
5.  **Query Engine:** Amazon Athena uses a schema defined with **OpenCSVSerde** to allow high-performance SQL queries directly on top of S3 without needing a traditional database.
    

🚀 Engineering Challenges & Solutions
-------------------------------------

### 1\. The "Comma" Conflict (Data Integrity)

**Problem:** Company names containing commas (e.g., "T-Mobile US, Inc.") were breaking the CSV structure during the ETL process, causing data to shift into the wrong columns in the analytics layer. **Solution:** Configured the Python ```csv.writer``` with ```quoting=csv.QUOTE_ALL``` and utilized the ```OpenCSVSerde``` library in Athena to ensure data integrity across the pipeline.

### 2\. Schema-on-Read Optimization

**Problem:** To perform mathematical analysis, the raw string data from S3 needed to be converted into numeric types without the overhead of a permanent database.
Solution: Developed a SQL View layer in Athena that performs dynamic type casting, converting string-based API outputs into ```DOUBLE``` and ```TIMESTAMP``` formats for real-time calculation.

3. Serverless Cost-Efficiencyessions.
    

### 3\. Serverless Cost-Efficiency

By utilizing Lambda and Athena instead of an EC2 instance or an RDS database, this pipeline follows a "pay-as-you-go" model, costing **$0.00** to run at low volumes while maintaining the ability to scale instantly.

🛠️ Tech Stack
--------------

*   **Cloud:** AWS (S3, Lambda, Athena, EventBridge, IAM).
    
*   **Languages:** Python 3.12 (Boto3, Urllib), SQL (Presto/Athena).
    
*   **Methodology:** Event-Driven Architecture, Data Lakehouse Design.
    


🛠️ SQL Sample
--------------
```text
CREATE OR REPLACE VIEW stock_analysis AS
SELECT 
    symbol,
    CAST(price AS DOUBLE) as stock_price,
    from_unixtime(CAST(timestamp AS BIGINT)) as trade_time,
    CAST(changesPercentage AS DOUBLE) as pct_change
FROM financial_data_table;

```

🛠️ Project Structure
-------------
```text
.
├── src/
│   ├── processor_lambda.py       # Transforming data
│   ├── producer.py               # Ingesting data
├── sql/
│   ├── athena_setup.sql          # Athena setup
├── README.md                     # Project documentation

```