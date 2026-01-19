"""
Configuration and constants.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# AlphaVantage API
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"

# Supabase Database
DB_CONFIG = {
    'host': os.getenv('SUPABASE_DB_HOST'),
    'database': os.getenv('SUPABASE_DB_NAME'),
    'user': os.getenv('SUPABASE_DB_USER'),
    'password': os.getenv('SUPABASE_DB_PASSWORD'),
    'port': os.getenv('SUPABASE_DB_PORT'),
    'sslmode': 'require'
}