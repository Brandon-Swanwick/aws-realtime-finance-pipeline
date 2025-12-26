Real-Time Financial Data Pipeline (AWS)
=======================================

🏗️ Architecture
----------------

An automated, event-driven ETL pipeline built on AWS to ingest, process, and visualize stock market data.

*   **Ingestion:** Python/Lambda triggered every 5 minutes by EventBridge.
    
*   **Storage:** S3 Data Lake (Bronze/Silver architecture).
    
*   **ETL:** Event-driven Python/Lambda for data cleaning and currency conversion.
    
*   **Analytics:** Amazon Athena (Serverless SQL) using OpenCSV SerDe.
    
*   **Visualization:** Amazon QuickSight dashboards.
    

📋 Prerequisites & Setup
------------------------

Before running the scripts, the following S3 buckets were created:

1.  raw-data-bucket: Stores incoming JSON/CSV from API.
    
2.  clean-data-bucket: Stores processed, analytics-ready CSVs.
    
3.  athena-queries-bucket: Dedicated for Athena query result storage.
    

🚀 Key Engineering Challenges Solved
------------------------------------

*   **Data Integrity:** Implemented OpenCSVSerde in Athena to handle complex string values containing commas (e.g., "T-Mobile US, Inc.").
    
*   **Serverless Scaling:** Utilized AWS Lambda and S3 to ensure the pipeline scales automatically.
    
*   **Type Safety:** Built a SQL view layer to cast string-based CSV data into proper Double and Timestamp types.
    

🛠️ Tech Stack
--------------

*   **AWS:** S3, Lambda, Athena, EventBridge, IAM, QuickSight.
    
*   **Language:** Python 3.12 (urllib, csv, boto3).