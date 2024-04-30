import json
import random
import requests
import textwrap
import urllib.parse

class QuoteFetcher:
    def __init__(self):
        pass


    def fetch_quote(self, file_path):
        with open(file_path, 'r') as file:
            quotes = json.load(file)
        selected_quote = random.choice(quotes)
        wrapped_quote = textwrap.fill(selected_quote["quote"], width=50)
        return f'"{wrapped_quote}"\n            - {selected_quote["author"]}'


    def fetch_quote_from_api(self, topic):
        try:
            # URL-encode the topic
            topic = urllib.parse.quote(topic)
            response = requests.get(f'https://api.quotable.io/random?tags={topic}')
            response.raise_for_status()
            data = response.json()
            wrapped_quote = textwrap.fill(data["content"], width=50)
            return f'"{wrapped_quote}"\n            - {data["author"]}'
        except requests.RequestException as e:
            print(f"An error occurred while fetching quote: {e}")
            return None