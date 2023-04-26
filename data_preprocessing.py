import pandas as pd
from sklearn.preprocessing import StandardScaler
from news_processing import preprocess_news_data

def preprocess_stock_data(stock_file_path):
    # Load historical stock data
    stock_data = pd.read_csv(stock_file_path)

    # Convert date string to datetime object
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])

    # Set date as index
    stock_data.set_index('Date', inplace=True)

    # Sort by date in ascending order
    stock_data = stock_data.sort_index(ascending=True)

    # Add daily returns as a feature
    stock_data['Daily_Returns'] = stock_data['Close'].pct_change()

    # Drop the first row with NaN values
    stock_data = stock_data.iloc[1:]

    return stock_data

def merge_data(stock_data, news_data):
    # Merge the historical stock data with the news sentiment scores
    merged_data = pd.merge(stock_data, news_data, how='left', left_index=True, right_index=True)

    # Forward fill the missing sentiment scores
    merged_data.fillna(method='ffill', inplace=True)

    return merged_data

def preprocess_data(stock_file_path, news_file_path):
    # Preprocess the historical stock data
    stock_data = preprocess_stock_data(stock_file_path)

    # Preprocess the news data
    news_data = preprocess_news_data(news_file_path)

    # Merge the historical stock data with the news sentiment scores
    merged_data = merge_data(stock_data, news_data)

    # Scale the features using StandardScaler
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(merged_data)

    # Split the data into training and testing datasets
    train_size = int(len(scaled_data) * 0.8)
    train_data, test_data = scaled_data[0:train_size,:], scaled_data[train_size:len(scaled_data),:]

    # Split the training and testing datasets into input and output variables
    X_train, y_train = train_data[:, 1:], train_data[:, 0]
    X_test, y_test = test_data[:, 1:], test_data[:, 0]

    return X_train, y_train, X_test, y_test, scaler
