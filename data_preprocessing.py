import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def load_data(file_path):
    data = pd.read_csv(file_path)
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.set_index('Date')
    return data

def merge_data(stock_data, news_data):
    news_df = pd.DataFrame({'News': news_data})
    news_df.index = stock_data.index
    merged = pd.concat([stock_data, news_df], axis=1)
    return merged

def preprocess_data(data):
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)
    return scaled_data

def split_data(data, test_size):
    train_size = int(len(data) * (1 - test_size))
    train_data, test_data = data[0:train_size,:], data[train_size:len(data),:]
    return train_data, test_data
