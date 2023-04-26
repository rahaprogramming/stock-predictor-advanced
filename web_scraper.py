import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

# Define the news sources to scrape
sources = [
    {'name': 'BBC', 'url': 'https://www.bbc.com/news/business'},
    {'name': 'CNN', 'url': 'https://www.cnn.com/business'},
    {'name': 'Reuters', 'url': 'https://www.reuters.com/finance'},
    {'name': 'Bloomberg', 'url': 'https://www.bloomberg.com/markets'},
    {'name': 'Yahoo Finance', 'url': 'https://finance.yahoo.com/'}
]

# Define the date range to scrape news articles for
start_date = datetime.now() - timedelta(days=7)
end_date = datetime.now()

# Define an empty DataFrame to store the results
df_news = pd.DataFrame(columns=['date', 'source', 'headline', 'article_text', 'stock_symbol'])

# Loop through each news source and scrape the news articles
for source in sources:
    print(f"Scraping news articles from {source['name']}...")
    response = requests.get(source['url'])
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article')
    for article in articles:
        # Extract the date, headline, and article text
        date_string = article.find('time')['datetime']
        date = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
        if date >= start_date and date <= end_date:
            headline = article.find('h3').text
            article_url = article.find('a')['href']
            article_response = requests.get(article_url)
            article_soup = BeautifulSoup(article_response.content, 'html.parser')
            article_text = '\n'.join([p.text for p in article_soup.find_all('p')])
            # Extract the stock symbol from the article text (if present)
            stock_symbol = None
            if 'stock' in article_text.lower():
                for word in article_text.lower().split():
                    if word.isupper() and len(word) <= 5:
                        stock_symbol = word
                        break
            # Append the results to the DataFrame
            df_news = df_news.append({'date': date, 'source': source['name'], 'headline': headline, 'article_text': article_text, 'stock_symbol': stock_symbol}, ignore_index=True)

# Save the results to a CSV file
df_news.to_csv('news_articles.csv', index=False)
