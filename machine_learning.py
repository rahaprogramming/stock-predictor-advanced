import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def train_model(X_train, y_train, model_type='linear'):
    if model_type == 'linear':
        model = LinearRegression()
    elif model_type == 'random_forest':
        model = RandomForestRegressor(n_estimators=100, random_state=42)
    elif model_type == 'svm':
        model = SVR(kernel='rbf', C=1000, gamma=0.1)

    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return {'MSE': mse, 'MAE': mae, 'R2': r2}

def predict_future_prices(model, X_future, scaler, news_score):
    X_future_scaled = scaler.transform(X_future)
    news_score_2d = np.array(news_score).reshape(1, -1)
    X_future_news = np.concatenate((X_future_scaled, news_score_2d), axis=1)
    future_prices = model.predict(X_future_news)
    return future_prices

