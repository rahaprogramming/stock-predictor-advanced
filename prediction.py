import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

def predict_stock_price(model_file, news_data_file, stock_data_file):
    # Load the saved model
    model = load_model(model_file)

    # Load the news data
    news_data = pd.read_csv(news_data_file)

    # Load the stock data
    stock_data = pd.read_csv(stock_data_file)

    # Merge the news data and stock data
    merged_data = pd.merge(news_data, stock_data, on=['date', 'symbol'])

    # Scale the features
    scaler = MinMaxScaler()
    merged_data['positive_sentiment'] = scaler.fit_transform(merged_data['positive_sentiment'].values.reshape(-1, 1))
    merged_data['negative_sentiment'] = scaler.fit_transform(merged_data['negative_sentiment'].values.reshape(-1, 1))
    merged_data['open'] = scaler.fit_transform(merged_data['open'].values.reshape(-1, 1))
    merged_data['high'] = scaler.fit_transform(merged_data['high'].values.reshape(-1, 1))
    merged_data['low'] = scaler.fit_transform(merged_data['low'].values.reshape(-1, 1))
    merged_data['close'] = scaler.fit_transform(merged_data['close'].values.reshape(-1, 1))
    merged_data['volume'] = scaler.fit_transform(merged_data['volume'].values.reshape(-1, 1))

    # Prepare the data for prediction
    X_test = merged_data.drop(['date', 'symbol', 'next_day_close'], axis=1).values
    X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

    # Predict the next day's closing stock price
    y_pred = model.predict(X_test)
    y_pred = scaler.inverse_transform(y_pred.reshape(-1, 1))

    # Return the predicted stock price
    return y_pred[-1][0]
