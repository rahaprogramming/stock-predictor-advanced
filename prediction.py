import pandas as pd
import numpy as np
import joblib
from datetime import datetime, timedelta
from news_processing import preprocess_news
from data_preprocessing import prepare_data_for_prediction

def predict_stock_price(stock_symbol, news_sources):
    # Load the trained model and scaler objects
    model = joblib.load('trained_model.pkl')
    scaler = joblib.load('scaler.pkl')

    # Get the latest news articles for the given stock symbol
    news_df = preprocess_news(stock_symbol, news_sources)

    # Prepare the data for prediction
    X_pred = prepare_data_for_prediction(news_df, scaler)

    # Predict the future stock prices
    future_dates = [datetime.now().date() + timedelta(days=i) for i in range(1, 8)]
    future_dates = pd.DataFrame(future_dates, columns=['Date'])
    future_dates['Symbol'] = stock_symbol
    X_pred = pd.concat([X_pred, future_dates], axis=0)
    X_pred.reset_index(inplace=True, drop=True)

    X_pred['Year'] = X_pred['Date'].apply(lambda x: x.year)
    X_pred['Month'] = X_pred['Date'].apply(lambda x: x.month)
    X_pred['Day'] = X_pred['Date'].apply(lambda x: x.day)

    X_pred = X_pred.drop('Date', axis=1)

    y_pred = model.predict(X_pred)

    # Return the predicted stock prices
    return y_pred[-7:]
