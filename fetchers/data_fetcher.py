"""
Functions for fetching stock data from AlphaVantage API.
"""
import requests
from config import ALPHA_VANTAGE_API_KEY, ALPHA_VANTAGE_BASE_URL


def fetch_daily_prices(symbol, outputsize='compact'):
    """
    Fetch daily price data for a stock symbol.
    
    Args:
        symbol: Stock ticker (e.g., 'AAPL')
        outputsize: 'compact' (100 days) or 'full' (20+ years)
    
    Returns:
        Dictionary of date -> price data, or None if error
    """
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': ALPHA_VANTAGE_API_KEY,
        'outputsize': outputsize
    }
    
    print(f"Fetching {symbol} from AlphaVantage...")
    
    try:
        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Check for errors
        if "Error Message" in data:
            print(f"API Error: {data['Error Message']}")
            return None
        
        if "Note" in data:
            print(f"Rate limit: {data['Note']}")
            return None
        
        if "Time Series (Daily)" not in data:
            print(f"Unexpected response: {data}")
            return None
        
        time_series = data['Time Series (Daily)']
        print(f"✓ Fetched {len(time_series)} days of data for {symbol}")
        
        return time_series
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None