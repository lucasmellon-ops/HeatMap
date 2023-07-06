import requests
import json
import pandas as pd
from geopy.geocoders import Nominatim
from textblob import TextBlob
import folium

def get_news_articles(api_key, keyword, language='en'):
    url = f"https://newsapi.org/v2/everything?q={keyword}&language={language}&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data['articles']

api_key = "yourAPIkey"
articles = get_news_articles(api_key, "shooting")

geolocator = Nominatim(user_agent="geoapiExercises")

data = []
for article in articles:
    title = article.get('title', 'Unknown')
    description = article.get('description', 'Unknown')
    location = article['source'].get('name', 'Unknown') if article.get('source') else 'Unknown'
    location_data = geolocator.geocode(location)
    if location_data:
        latitude = location_data.latitude
        longitude = location_data.longitude
    else:
        latitude = None
        longitude = None
    sentiment = TextBlob(description).sentiment
    polarity = sentiment.polarity
    data.append([title, description, location, latitude, longitude, polarity])

df = pd.DataFrame(data, columns=['title', 'description', 'location', 'latitude', 'longitude', 'polarity'])

m = folium.Map(location=[0, 0], zoom_start=2)

for index, row in df.iterrows():
    if pd.notna(row['latitude']) and pd.notna(row['longitude']):
        if row['polarity'] > 0:
            marker_color = 'green'
        elif row['polarity'] < 0:
            marker_color = 'red'
        else:
            marker_color = 'beige'
        folium.Marker(
            [row['latitude'], row['longitude']], 
            popup=f"Title: {row['title']}, Polarity: {row['polarity']}",
            icon=folium.Icon(color=marker_color),
        ).add_to(m)

# Save map to desktop
m.save('C:/Users/Lucas/Desktop/map.html')

