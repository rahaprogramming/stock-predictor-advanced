# File 2: predict_stock_prices.py
# Predict stock prices for stocks mentioned in the scraped news articles

import pandas as pd
import yfinance as yf
from textblob import TextBlob
from sklearn.linear_model import LinearRegression

# Define the start and end dates for the historical data
start_date = '2010-01-01'
end_date = pd.Timestamp.now().strftime('%Y-%m-%d')

# Load the historical stock prices dataframe from the CSV file
stock_prices = pd.read_csv('stock_prices.csv')

# Add sentiment analysis data to the stock prices dataframe
stock_prices['Sentiment'] = 0.0

# Define the list of news sources to scrape data from
news_sources = ['CNN', 'BBC', 'Reuters', 'Bloomberg', 'CNBC']

# Define a function to perform sentiment analysis on a given news article
def analyze_sentiment(article):
    """
    Analyze the sentiment of a news article using TextBlob
    
    Parameters:
    article (str): The news article text to analyze
    
    Returns:
    float: The sentiment polarity score between -1.0 and 1.0
    """
    blob = TextBlob(article)
    return blob.sentiment.polarity

# Loop through each news source and scrape articles for the current date
for source in news_sources:
    # Scrape news articles from the current date
    url = f'https://newsapi.org/v2/everything?q=stock&from={end_date}&to={end_date}&sources={source}&apiKey=YOUR_API_KEY'
    articles = requests.get(url).json()['articles']
    
    # Loop through each article and analyze the sentiment
    for article in articles:
        # Check if the article mentions any of the stocks in the stock_prices dataframe
        for symbol in stock_prices['Symbol'].unique():
            if symbol in article['title'] or symbol in article['description']:
                # If the stock is mentioned, perform sentiment analysis on the article and update the stock_prices dataframe
                sentiment = analyze_sentiment(article['content'])
                stock_prices.loc[(stock_prices['Symbol'] == symbol) & (stock_prices.index == end_date), 'Sentiment'] = sentiment
                print(f"Article from {source} found for {symbol} on {end_date}. Sentiment: {sentiment:.2f}")
                break

# Drop any rows with missing data (i.e. stocks that were not mentioned in any news articles)
stock_prices.dropna(inplace=True)

# Split the data into training and testing sets
train_data = stock_prices[stock_prices.index < end_date]
test_data = stock_prices[stock_prices.index == end_date]

# Define the features and target variable for the linear regression model
X_train = train_data[['Sentiment']]
y_train = train_data['Close']
X_test = test_data[['Sentiment']]
y_test = test_data['Close']

# Fit a linear regression model to the training data
model = LinearRegression()
model.fit(X_train, y_train)

# Predict the stock prices for the testing data
y_pred = model.predict(X_test)

# Print the predicted stock prices for each stock mentioned in the news articles
for symbol in stock_prices['Symbol'].unique():
    if symbol in test_data['Symbol'].unique():
        pred_price = y_pred[test_data['Symbol'] == symbol][0]
        print(f"Predicted closing price for {symbol} on {end_date}: {pred_price:.2f}")
