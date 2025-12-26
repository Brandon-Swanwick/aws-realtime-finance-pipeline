import json
import boto3
import io
import csv
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Triggered by S3 Upload. Performs data cleaning,  currency conversion (USD to CAD), and saves to the 'Silver' layer.
    
    # 1. Parse source info from S3 Event
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    source_key = event['Records'][0]['s3']['object']['key']
    
    # Define destination (Silver Layer)
    dest_bucket = source_bucket.replace("-raw-", "-clean-")
    dest_key = f"processed/{os.path.basename(source_key)}"
    
    # 2. Download the raw file
    response = s3.get_object(Bucket=source_bucket, Key=source_key)
    content = response['Body'].read().decode('utf-8')
    
    # 3. Read and Transform data
    # DictReader automatically handles the header row
    reader = csv.DictReader(io.StringIO(content))
    cleaned_rows = []
    
    # Business Logic: Simple currency conversion
    EXCHANGE_RATE_CAD = 1.35 
    
    for row in reader:
        try:
            usd_price = float(row['price'])
            cleaned_rows.append({
                "symbol": row['symbol'],
                "name": row['name'],
                "timestamp": row['timestamp'],
                "price_usd": round(usd_price, 2),
                "price_cad": round(usd_price * EXCHANGE_RATE_CAD, 2)
            })
        except ValueError:
            continue
        
    # 4. Write to CSV using OpenCSV standards (Minimal Quoting)
    output = io.StringIO()
    fieldnames = ["symbol", "name", "timestamp", "price_usd", "price_cad"]
    writer = csv.DictWriter(output, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
    
    writer.writeheader()
    writer.writerows(cleaned_rows)
    
    # 5. Upload processed data to Clean Bucket
    s3.put_object(
        Bucket=dest_bucket, 
        Key=dest_key, 
        Body=output.getvalue()
    )
    
    return {
        "status": "Success",
        "processed_file": dest_key,
        "records_count": len(cleaned_rows)
    }