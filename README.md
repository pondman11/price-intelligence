# Price Intelligence System

A data pipeline project that integrates multiple financial data sources, performs data cleaning and transformation, and applies machine learning for price prediction and analysis.

## Project Overview

This project demonstrates:
- Multi-source data integration (stocks, crypto, trends)
- ETL pipeline development
- Data quality and validation
- Machine learning applications
- RESTful API deployment

## Prerequisites

- Python 3.10 or higher
- Git
- AlphaVantage API key (free tier available)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/price-intelligence.git
cd price-intelligence
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt when activated.

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

1. Copy the example environment file:
```bash
   # Windows
   copy .env.example .env
   
   # Mac/Linux
   cp .env.example .env
```

2. Edit `.env` and add your API keys:
```
   ALPHA_VANTAGE_API_KEY=your_actual_api_key_here
```

3. Get a free AlphaVantage API key:
   - Visit: https://www.alphavantage.co/support/#api-key
   - Enter your email
   - Copy the key to your `.env` file

### 5. Test the Setup

Run the API test script:
```bash
python test_api.py
```

You should see stock data for IBM printed to the console.

## Project Structure
```
price-intelligence/
├── .env                    # API keys (not in git)
├── .env.example           # Template for API keys
├── .gitignore             # Git ignore rules
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── test_api.py           # API connection test
└── venv/                 # Virtual environment (not in git)
```

## Usage

### Running the Test Script
```bash
# Make sure venv is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Run the test
python test_api.py
```

## API Information

### AlphaVantage
- **Free Tier Limits**: 25 requests/day, 5 requests/minute
- **Documentation**: https://www.alphavantage.co/documentation/

## Development Workflow

### Making Changes

1. Create a new branch:
```bash
   git checkout -b feature/your-feature-name
```

2. Make your changes

3. Commit and push:
```bash
   git add .
   git commit -m "Description of changes"
   git push origin feature/your-feature-name
```

4. Create a Pull Request on GitHub

### Updating Dependencies

If you install new packages:
```bash
pip install package-name
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Add new dependency: package-name"
```

## Troubleshooting

### "Module not found" errors
- Make sure your virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### API errors
- Check your `.env` file has the correct API key
- Verify you haven't exceeded rate limits (25 calls/day)
- Check API status: https://www.alphavantage.co/support/#support

### Git issues
- Make sure `.env` is in `.gitignore` (never commit API keys!)
- If you see `venv/` in git status, it should be ignored by `.gitignore`

## Contributing

This is a portfolio project, but feedback and suggestions are welcome! Please open an issue to discuss proposed changes.

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

- GitHub: [@pondman11](https://github.com/pondman11)



## Next Steps

Planned features:
- [ ] Add multiple data sources (CoinGecko, Google Trends)
- [ ] Implement data storage (PostgreSQL/SQLite)
- [ ] Build ETL pipeline with Airflow
- [ ] Create ML models for price prediction
- [ ] Deploy FastAPI REST API
- [ ] Add visualization dashboard