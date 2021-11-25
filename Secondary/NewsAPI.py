#NewsAPI
import requests
GET= 'https://newsapi.org/v2/everything?q=keyword&apiKey=5b0e1fcdbd944762b51dd5e1bd2efa56'
g = requests.get(GET)

g.json()
