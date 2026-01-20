"""
Functions for storing and retrieving data from Supabase.
"""
import os
import psycopg2
from config import DB_CONFIG


def get_connection():
    """Get a database connection."""
    return psycopg2.connect(**DB_CONFIG)


def init_database():
    """Verify Terraform-managed tables exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Read schema from SQL file
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
    
    # Execute the schema SQL
    # Note: psycopg2 can handle multiple statements separated by semicolons
    cursor.execute(schema_sql)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✓ Database initialized")


def save_stock_data(symbol, time_series):
    """
    Save stock price data to database.
    
    Args:
        symbol: Stock ticker
        time_series: Dictionary of date -> price data from AlphaVantage
    
    Returns:
        Number of records inserted
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Insert/update stock metadata
        cursor.execute('''
            INSERT INTO stocks (symbol, last_updated)
            VALUES (%s, CURRENT_TIMESTAMP)
            ON CONFLICT (symbol) 
            DO UPDATE SET last_updated = CURRENT_TIMESTAMP
        ''', (symbol,))
        
        # Insert price data
        inserted = 0
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
            if cursor.rowcount > 0:
                inserted += 1
        
        conn.commit()
        print(f"✓ Saved {inserted} records for {symbol}")
        return inserted
        
    except Exception as e:
        conn.rollback()
        print(f"Error saving data: {e}")
        return 0
    finally:
        cursor.close()
        conn.close()


def get_recent_prices(symbol, days=5):
    """
    Get recent price data for a symbol.
    
    Args:
        symbol: Stock ticker
        days: Number of recent days to retrieve
    
    Returns:
        List of tuples (date, open, high, low, close, volume)
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT date, open, high, low, close, volume
        FROM daily_prices
        WHERE symbol = %s
        ORDER BY date DESC
        LIMIT %s
    ''', (symbol, days))
    
    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return rows


def get_all_symbols():
    """Get list of all symbols in database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT symbol FROM stocks ORDER BY symbol')
    symbols = [row[0] for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    return symbols