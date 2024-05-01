import json
import random
import requests
import textwrap
import urllib.parse

class QuoteFetcher:
    def __init__(self):
        self.tags = self.fetch_tags()

    def fetch_tags(self):
        with open('config/quotable_tags.json') as f:
            data = json.load(f)
        tag_dict = {item[0]: item[1] for item in data}
        return tag_dict


    def fetch_quote(self, file_path):
        with open(file_path, 'r') as file:
            quotes = json.load(file)
        selected_quote = random.choice(quotes)
        wrapped_quote = textwrap.fill(selected_quote["quote"], width=50)
        return f'"{wrapped_quote}"\n            - {selected_quote["author"]}'

    def fetch_quote_from_api(self, tag):
        try:
            # URL-encode the tag
            tag = urllib.parse.quote(tag)
            response = requests.get(f'https://api.quotable.io/random?tags={tag}')
            response.raise_for_status()
            data = response.json()
            wrapped_quote = textwrap.fill(data["content"], width=50)
            return f'"{wrapped_quote}"\n            - {data["author"]}'
        except requests.RequestException as e:
            print(f"An error occurred while fetching quote: {e}")
            return None
        
    def user_entered_quote(self, quote, author):
        wrapped_quote = textwrap.fill(quote, width=50)
        if author:
            return f'"{wrapped_quote}"\n            - {author}'
        else:
            return f'"{wrapped_quote}"'