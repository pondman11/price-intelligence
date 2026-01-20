-- Database schema for Price Intelligence System
-- This file contains the table and index definitions that can be managed
-- by infrastructure-as-code tools like Terraform

-- Stocks table: stores metadata for each stock symbol
CREATE TABLE IF NOT EXISTS stocks (
    symbol TEXT PRIMARY KEY,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Daily prices table: stores daily OHLCV data for stocks
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
);

-- Index for faster queries on symbol and date
CREATE INDEX IF NOT EXISTS idx_daily_prices_symbol_date 
ON daily_prices(symbol, date DESC);
