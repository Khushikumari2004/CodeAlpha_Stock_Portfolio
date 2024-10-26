from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(_name_)

# Get API key from environment variable
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

# In-memory portfolio
portfolio = []

def get_stock_data(symbol):
    """Fetch stock data from Alpha Vantage."""
    url = f'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '5min',
        'apikey': ALPHA_VANTAGE_API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()

        # Parse the latest stock price
        time_series = data.get('Time Series (5min)')
        if time_series:
            latest_time = list(time_series.keys())[0]
            latest_price = float(time_series[latest_time]['4. close'])
            return latest_price
        return None
    except Exception as e:
        return str(e)

@app.route('/portfolio/add', methods=['POST'])
def add_stock():
    """Add a stock to the portfolio."""
    data = request.json
    symbol = data.get('symbol')
    quantity = data.get('quantity')
    purchase_price = data.get('purchasePrice')

    if not symbol or quantity <= 0 or purchase_price <= 0:
        return jsonify({"error": "Invalid input. Please check your data."}), 400

    portfolio.append({'symbol': symbol, 'quantity': quantity, 'purchasePrice': purchase_price})
    return jsonify({"message": f"Stock {symbol} added to portfolio.", "portfolio": portfolio})

@app.route('/portfolio/remove/<string:symbol>', methods=['DELETE'])
def remove_stock(symbol):
    """Remove a stock from the portfolio."""
    global portfolio
    portfolio = [stock for stock in portfolio if stock['symbol'].upper() != symbol.upper()]
    return jsonify({"message": f"Stock {symbol} removed from portfolio.", "portfolio": portfolio})

@app.route('/portfolio', methods=['GET'])
def get_portfolio():
    """Get the current portfolio with updated stock prices."""
    total_investment = 0
    total_current_value = 0
    updated_portfolio = []

    for stock in portfolio:
        latest_price = get_stock_data(stock['symbol'])
        if latest_price is not None:
            stock_value = latest_price * stock['quantity']
            total_investment += stock['purchasePrice'] * stock['quantity']
            total_current_value += stock_value
            stock.update({'latestPrice': latest_price, 'currentValue': stock_value})
        updated_portfolio.append(stock)

    return jsonify({
        "portfolio": updated_portfolio,
        "totalInvestment": total_investment,
        "totalCurrentValue": total_current_value,
        "profitLoss": total_current_value - total_investment
    })

if _name_ == '_main_':
    app.run(debug=True)