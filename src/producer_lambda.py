import json
import boto3
import urllib.request
from datetime import datetime

# Initialize S3 client
s3 = boto3.client('s3')

# Raw bucket name
BUCKET_NAME = "brandon-swanwick-finance-raw-1313" 

def lambda_handler(event, context):
    # Ingests real-time stock data from Yahoo Finance API and saves the raw CSV to the 'Bronze' layer of the S3 Data Lake.

    stocks = ["NVDA", "JPM", "LLY", "TSM", "COST", "XOM", "CAT", "SHOP", "TMUS", "RY"]
    collected = []
    
    print(f"Starting ingestion for {len(stocks)} symbols...")
    
    for symbol in stocks:
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1m&range=1d"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                meta = data['chart']['result'][0]['meta']
                
                collected.append({
                    "symbol": symbol,
                    "name": meta.get('longName', symbol),
                    "price": meta.get('regularMarketPrice'),
                    "timestamp": datetime.now().isoformat()
                })
        except Exception as e:
            print(f"Error fetching {symbol}: {str(e)}")

    # Construct CSV content with quoted names to handle commas (e.g., "T-Mobile US, Inc.")
    csv_out = "symbol,name,price,timestamp\n"
    for item in collected:
        # We wrap the name in double quotes for CSV safety
        csv_out += f"{item['symbol']},\"{item['name']}\",{item['price']},{item['timestamp']}\n"

    # Generate unique filename based on current time
    file_name = f"stocks/stock_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    # Upload to S3
    s3.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=csv_out)
    
    return {
        "status": "200 OK",
        "file_uploaded": file_name,
        "count": len(collected)
    }