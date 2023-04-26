# File 1: collect_stock_prices.py
# Collect historical stock price data for the top 100 performing stocks

import pandas as pd
import yfinance as yf

# Define the list of stock symbols to collect data for
symbols = ['AAPL', 'GOOG', 'AMZN', 'FB', 'TSLA', 'MSFT', 'NVDA', 'JPM', 'JNJ', 'V', 'UNH', 'PG', 'MA', 'HD', 'DIS', 'NFLX', 'BAC', 'VZ', 'PYPL', 'KO', 'PFE', 'INTC', 'PEP', 'MRK', 'WMT', 'CSCO', 'ABT', 'ABBV', 'CVS', 'CMCSA', 'T', 'XOM', 'BA', 'MCD', 'IBM', 'TXN', 'QCOM', 'NEE', 'NKE', 'ORCL', 'MMM', 'ACN', 'AMGN', 'HON', 'CHTR', 'UNP', 'DHR', 'SPGI', 'LIN', 'TMUS', 'COST', 'CRM', 'GE', 'NOW', 'GS', 'CAT', 'AXP', 'SLB', 'USB', 'TMO', 'FDX', 'BLK', 'BMY', 'INTU', 'PLD', 'AMAT', 'AMD', 'CI', 'DUK', 'EOG', 'BAX', 'DE', 'LMT', 'EMR', 'APD', 'APTV', 'GILD', 'ADBE', 'CVX', 'MDT', 'MMM', 'CME', 'DUK', 'SLB', 'COP', 'BKNG', 'SPG', 'LOW', 'ETN', 'DOW', 'SYK', 'SO', 'BK', 'CCI', 'AIG', 'WM', 'SO', 'GM', 'WFC']

# Define the start and end dates for the historical data
start_date = '2010-01-01'
end_date = pd.Timestamp.now().strftime('%Y-%m-%d')

# Create an empty dataframe to store the historical stock prices
stock_prices = pd.DataFrame()

# Collect historical stock prices for each symbol and append to the stock_prices dataframe
for symbol in symbols:
    data = yf.download(symbol, start=start_date, end=end_date)
    data['Symbol'] = symbol
    stock_prices = stock_prices.append(data)

# Save the stock prices dataframe to a CSV file
stock_prices.to_csv('stock_prices.csv', index=False)
