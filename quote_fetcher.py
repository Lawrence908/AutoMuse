import json
import random

class QuoteFetcher:
    def __init__(self, file_path):
        self.file_path = file_path

    def fetch_quote(self):
        with open(self.file_path, 'r') as file:
            quotes = json.load(file)
        selected_quote = random.choice(quotes)
        return f'"{selected_quote["quote"]}"\n - {selected_quote["author"]}'