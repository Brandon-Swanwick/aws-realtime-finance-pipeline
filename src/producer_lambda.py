import json
import boto3
import urllib.request
from datetime import datetime

# Initialize S3 client
s3 = boto3.client('s3')

# Replace with your actual raw bucket name
BUCKET_NAME = "brandon-swanwick-finance-raw-1313" 

def lambda_handler(event, context):
    """
    Ingests real-time stock data from Yahoo Finance API 
    including Price and Percent Change.
    """
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
                    "pct_change": meta.get('regularMarketChangePercent', 0.0), # Added this
                    "timestamp": datetime.now().isoformat()
                })
        except Exception as e:
            print(f"Error fetching {symbol}: {str(e)}")

    # Updated headers to include pct_change
    csv_out = "symbol,name,price,pct_change,timestamp\n"
    for item in collected:
        csv_out += f"{item['symbol']},\"{item['name']}\",{item['price']},{item['pct_change']},{item['timestamp']}\n"

    file_name = f"stocks/stock_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    s3.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=csv_out)
    
    return {"status": "200 OK", "count": len(collected)}