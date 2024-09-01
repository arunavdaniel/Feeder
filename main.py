import feedparser
import pandas as pd
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

df = pd.read_csv('rss_feeds.csv', header=None)
column_data = df[0].tolist()

all_entries = []

for url in column_data:
    d = feedparser.parse(url)

    for entry in d.entries:
        r = requests.get(entry.link)
        sp = r.text
        soup = BeautifulSoup(sp, 'html.parser')

        tag_names = ['p', 'h1', 'h2', 'h3', 'h4']
        fulltext = ''
        
        for tag_name in tag_names:
            tags = soup.find_all(tag_name)
            for tag in tags:
                object = tag.text
                fulltext += object

        fulltext_without_space = fulltext.replace('\n', '').replace('\r', '').replace('\t', '').strip()

        blob = TextBlob(fulltext_without_space)
        sentiment = blob.sentiment.polarity

        all_entries.append({
            'title': entry.title,
            'link': entry.link,
            'content': fulltext_without_space,
            'sentiment': sentiment
        })

df_final = pd.DataFrame(all_entries)
df_final.to_csv('rss_feed_with_content_and_sentiment.csv', index=False)
