import re
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from textblob import TextBlob

def clean_text(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub('[‘’“”…]', '', text)
    text = re.sub('\n', '', text)
    return text

def preprocess_news(news):
    processed_news = []
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()
    for headline in news:
        cleaned = clean_text(headline)
        words = cleaned.split()
        stemmed_words = [ps.stem(word) for word in words if not word in stop_words]
        processed_news.append(' '.join(stemmed_words))
    return processed_news

def analyze_sentiment(news):
    sentiment_scores = []
    for headline in news:
        text = TextBlob(headline)
        score = text.sentiment.polarity
        sentiment_scores.append(score)
    return sentiment_scores
