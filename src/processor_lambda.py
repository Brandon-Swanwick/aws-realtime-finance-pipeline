import json
import boto3
import io
import csv
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    source_key = event['Records'][0]['s3']['object']['key']
    
    dest_bucket = source_bucket.replace("-raw-", "-clean-")
    dest_key = f"processed/{os.path.basename(source_key)}"
    
    response = s3.get_object(Bucket=source_bucket, Key=source_key)
    content = response['Body'].read().decode('utf-8')
    
    reader = csv.DictReader(io.StringIO(content))
    cleaned_rows = []
    
    EXCHANGE_RATE_CAD = 1.35 
    
    for row in reader:
        try:
            usd_price = float(row['price'])
            # Percent change is a float already, we just pass it through
            pct_change = float(row['pct_change']) if row.get('pct_change') else 0.0
            
            cleaned_rows.append({
                "symbol": row['symbol'],
                "name": row['name'],
                "timestamp": row['timestamp'],
                "price_usd": round(usd_price, 2),
                "price_cad": round(usd_price * EXCHANGE_RATE_CAD, 2),
                "pct_change": round(pct_change, 2)
            })
        except (ValueError, KeyError):
            continue
        
    output = io.StringIO()
    fieldnames = ["symbol", "name", "timestamp", "price_usd", "price_cad", "pct_change"]
    writer = csv.DictWriter(output, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
    
    writer.writeheader()
    writer.writerows(cleaned_rows)
    
    s3.put_object(Bucket=dest_bucket, Key=dest_key, Body=output.getvalue())
    
    return {"status": "Success", "records_count": len(cleaned_rows)}