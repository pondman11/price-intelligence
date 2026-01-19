"""
Simple script to fetch one stock from AlphaVantage and store in Supabase.
"""
import requests
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_connection():
    """Connect to Supabase database."""
    conn = psycopg2.connect(
        host=os.getenv('SUPABASE_DB_HOST'),
        database=os.getenv('SUPABASE_DB_NAME'),
        user=os.getenv('SUPABASE_DB_USER'),
        password=os.getenv('SUPABASE_DB_PASSWORD'),
        port=os.getenv('SUPABASE_DB_PORT'),
        sslmode='require'
    )
    return conn

def create_tables():
    """Create tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create stocks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            symbol TEXT PRIMARY KEY,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create daily_prices table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_prices (
            id SERIAL PRIMARY KEY,
            symbol TEXT NOT NULL,
            date DATE NOT NULL,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            volume BIGINT NOT NULL,
            UNIQUE(symbol, date)
        )
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✓ Tables created")

def fetch_stock_data(symbol):
    """Fetch stock data from AlphaVantage."""
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    
    url = "https://www.alphavantage.co/query"
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': api_key,
        'outputsize': 'compact'  # Last 100 days
    }
    
    print(f"Fetching data for {symbol}...")
    response = requests.get(url, params=params)
    data = response.json()
    
    if "Time Series (Daily)" not in data:
        print(f"Error: {data}")
        return None
    
    return data['Time Series (Daily)']

def store_stock_data(symbol, time_series):
    """Store stock data in Supabase."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert stock metadata
    cursor.execute('''
        INSERT INTO stocks (symbol, last_updated)
        VALUES (%s, CURRENT_TIMESTAMP)
        ON CONFLICT (symbol) DO UPDATE SET last_updated = CURRENT_TIMESTAMP
    ''', (symbol,))
    
    # Insert price data
    count = 0
    for date_str, values in time_series.items():
        cursor.execute('''
            INSERT INTO daily_prices (symbol, date, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (symbol, date) DO NOTHING
        ''', (
            symbol,
            date_str,
            float(values['1. open']),
            float(values['2. high']),
            float(values['3. low']),
            float(values['4. close']),
            int(values['5. volume'])
        ))
        count += 1
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✓ Stored {count} records for {symbol}")

def verify_data(symbol):
    """Check what's in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT date, close, volume 
        FROM daily_prices 
        WHERE symbol = %s 
        ORDER BY date DESC 
        LIMIT 5
    ''', (symbol,))
    
    rows = cursor.fetchall()
    
    print(f"\nMost recent 5 days for {symbol}:")
    for row in rows:
        date, close, volume = row
        print(f"  {date}: ${close:.2f}, Volume: {volume:,}")
    
    cursor.close()
    conn.close()

def main():
    print("="*50)
    print("FETCH AND STORE SINGLE STOCK")
    print("="*50)
    
    # Step 1: Create tables
    create_tables()
    
    # Step 2: Fetch data
    symbol = 'AAPL'  # Apple stock
    time_series = fetch_stock_data(symbol)
    
    if time_series:
        # Step 3: Store data
        store_stock_data(symbol, time_series)
        
        # Step 4: Verify
        verify_data(symbol)
        
        print("\n" + "="*50)
        print("✓ SUCCESS!")
        print("="*50)
    else:
        print("✗ Failed to fetch data")

if __name__ == "__main__":
    main()