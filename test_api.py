import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

def test_alpha_vantage():
    """Simple test to fetch stock data from AlphaVantage API"""
    
    # Get API key from environment
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    
    if not api_key:
        print("ERROR: API key not found. Check your .env file")
        return
    
    # AlphaVantage endpoint for daily stock data
    base_url = "https://www.alphavantage.co/query"
    
    # Parameters for the API call
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': 'IBM',
        'apikey': api_key,
        'outputsize': 'compact'
    }
    
    print(f"Fetching data for {params['symbol']}...")
    
    try:
        # Make the API request
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        
        # Check for errors
        if "Error Message" in data:
            print(f"API Error: {data['Error Message']}")
            return
        
        if "Note" in data:
            print(f"Rate limit note: {data['Note']}")
            return
        
        # Print results
        print("\n✓ Successfully fetched data!")
        print(f"\nMetadata:")
        print(json.dumps(data.get('Meta Data', {}), indent=2))
        
        # Get time series data
        time_series = data.get('Time Series (Daily)', {})
        
        if time_series:
            print(f"\nMost recent 5 days of data:")
            for date in list(time_series.keys())[:5]:
                day_data = time_series[date]
                print(f"\n{date}:")
                print(f"  Open: ${day_data['1. open']}")
                print(f"  High: ${day_data['2. high']}")
                print(f"  Low: ${day_data['3. low']}")
                print(f"  Close: ${day_data['4. close']}")
                print(f"  Volume: {day_data['5. volume']}")
        else:
            print("No time series data found")
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    test_alpha_vantage()