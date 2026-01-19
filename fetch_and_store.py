"""
Main script to fetch stock data and store in database.
"""
from fetchers.data_fetcher import fetch_daily_prices
from storage.data_storage import init_database, save_stock_data, get_recent_prices


def main():
    print("="*50)
    print("FETCH AND STORE STOCK DATA")
    print("="*50)
    
    # Initialize database
    init_database()
    
    # Fetch data
    symbol = 'IBM'
    time_series = fetch_daily_prices(symbol)
    
    if time_series:
        # Store data
        save_stock_data(symbol, time_series)
        
        # Show recent prices
        print(f"\nMost recent 5 days for {symbol}:")
        recent = get_recent_prices(symbol, days=5)
        for date, open_p, high, low, close, volume in recent:
            print(f"  {date}: ${close:.2f} (Vol: {volume:,})")
        
        print("\n" + "="*50)
        print("✓ SUCCESS!")
        print("="*50)
    else:
        print("✗ Failed to fetch data")


if __name__ == "__main__":
    main()