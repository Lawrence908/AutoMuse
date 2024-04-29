import os
import requests

class MediaFetcher:
    def __init__(self, access_key):
        self.access_key = os.getenv("UNSPLASH_ACCESS_KEY")

    def fetch_image(self, query="nature", per_page=10):
        url = f"https://api.unsplash.com/search/photos?query={query}&per_page={per_page}"
        headers = {"Authorization": f"Client-ID {self.access_key}"}
        response = requests.get(url, headers=headers)
        data = response.json()

        # The API returns a list of photos. Let's just return the first one.
        if data["results"]:
            return data["results"][0]["urls"]["full"]

    def fetch_video(self):
        pass