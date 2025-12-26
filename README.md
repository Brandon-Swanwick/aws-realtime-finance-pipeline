Real-Time Financial Data Pipeline (AWS Serverless)
==================================================

An automated, event-driven ETL (Extract, Transform, Load) pipeline built on AWS to ingest, process, and query real-time stock market data. This project demonstrates the ability to build scalable cloud infrastructure that handles raw API data and transforms it into analytics-ready SQL tables.

🏗️ Architecture & Data Flow
----------------------------

1.  **Ingestion (The Producer):** An AWS Lambda function triggered every 5 minutes by **Amazon EventBridge**. It fetches real-time stock quotes (Price, Change, Volume) via the Financial Modeling Prep API.
    
2.  **Raw Storage (Bronze):** Data is stored in its original format in the raw-data-bucket for auditing and historical replay.
    
3.  **Transformation (The Consumer):** An S3-triggered Lambda function detects the new file, cleans the headers, performs currency conversions, and handles edge cases (like commas in company names).
    
4.  **Analytics Layer (Silver):** The processed data is saved to the clean-data-bucket in a flat CSV format optimized for **Amazon Athena**.
    
5.  **Query Engine:** Amazon Athena uses a schema defined with **OpenCSVSerde** to allow high-performance SQL queries directly on top of S3 without needing a traditional database.
    

🚀 Engineering Challenges & Solutions
-------------------------------------

### 1\. The "Comma" Conflict (Data Integrity)

**Problem:** Company names like "T-Mobile US, Inc." contained commas, which broke standard CSV parsing in SQL, causing the price data to shift into the wrong columns.**Solution:** Implemented the OpenCSVSerde library in Athena and updated the Python Lambda to wrap string fields in quotes, ensuring 100% data alignment.

### 2\. Schema-on-Read Optimization

**Problem:** S3 stores everything as flat files, which Athena initially reads as strings.**Solution:** Developed a SQL View layer that performs dynamic type casting:

*   Converted Price from STRING to DOUBLE.
    
*   Converted Timestamp from UNIX to TIMESTAMP format.
    
*   Calculated "Market Volatility" metrics on the fly using SQL expressions.
    

### 3\. Serverless Cost-Efficiency

By utilizing Lambda and Athena instead of an EC2 instance or an RDS database, this pipeline costs **$0.00** to run at low volumes, scaling only when data throughput increases.

🛠️ Tech Stack
--------------

*   **Cloud:** AWS (S3, Lambda, Athena, EventBridge, IAM).
    
*   **Languages:** Python 3.12 (Boto3, Urllib), SQL (Presto/Athena).
    
*   **Methodology:** Event-Driven Architecture, Data Lakehouse Design.
    

📊 SQL Sample
-------------

To analyze the data, I used the following Athena transformation:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   CREATE OR REPLACE VIEW stock_analysis AS  SELECT       symbol,      CAST(price AS DOUBLE) as stock_price,      from_unixtime(CAST(timestamp AS BIGINT)) as trade_time,      CAST(changesPercentage AS DOUBLE) as pct_change  FROM financial_data_table;   `