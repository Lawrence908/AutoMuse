import os
import io
import json
import random
import requests
from PIL import Image

class MediaFetcher:
    def __init__(self, image_query="nature", platform="instagram"):
        self.access_key = os.getenv("UNSPLASH_ACCESS_KEY")

        #Load the unsplash_queries.json file
        with open('config/unsplash_queries.json') as f:
            self.queries = json.load(f)

        # Load the platform dimensions from the JSON file
        with open('config/platform_dimensions.json') as f:
            self.platform_dimensions = json.load(f)
        self.platform = platform
        self.aspect_ratio, self.max_dimension = self.platform_dimensions.get(platform)
        self.image_query = image_query

    def download_image(self, image_url, filename):
        # Download the image
        response = requests.get(image_url)
        image = Image.open(io.BytesIO(response.content))
        
        # Save the image
        image.save(filename)

    def resize_image(self, image_path, platform, filename):
        # Open the image
        image = Image.open(image_path)
        print(f"Resizing image for platform '{platform}'")
        self.aspect_ratio, self.max_dimension = self.platform_dimensions.get(platform)
        

        if self.aspect_ratio and self.max_dimension:
            # Calculate the aspect ratio of the image and the target size
            image_aspect_ratio = image.width / image.height
            target_aspect_ratio = self.aspect_ratio[0] / self.aspect_ratio[1]

            # Crop the image to the target aspect ratio
            if image_aspect_ratio > target_aspect_ratio:
                new_width = image.height * target_aspect_ratio
                left = (image.width - new_width) / 2
                right = (image.width + new_width) / 2
                image = image.crop((left, 0, right, image.height))
            else:
                new_height = image.width / target_aspect_ratio
                top = (image.height - new_height) / 2
                bottom = (image.height + new_height) / 2
                image = image.crop((0, top, image.width, bottom))

            # Calculate the scaling factor
            scaling_factor = self.max_dimension / max(image.width, image.height)

            # Resize image to maximum dimension
            new_size = (int(image.width * scaling_factor), int(image.height * scaling_factor))
            image = image.resize(new_size, Image.LANCZOS)

        # Save the resized image
        image.save(filename)

    def download_and_resize_image(self, image_url, platform, filename):
        # Download the image
        self.download_image(image_url, filename)

        # Resize the downloaded image
        self.resize_image(filename, platform, filename)

    def fetch_image(self, platform, per_page=10):
        self.platform = platform
        print(f"Fetching images for query: {self.image_query}")
        print(f"Platform: {self.platform}")

        # Get a random page from 1 to the total number of pages for that query
        query_total = self.queries.get(self.image_query)
        if query_total is None:
            raise ValueError('Invalid query')
        query_pages = (query_total // per_page)
        page = 1
        if query_total > 1:
            page = random.randint(1, max(1, int(0.8*query_pages)))

        print(f"Fetching page {page} of {query_pages}")

        url = f"https://api.unsplash.com/search/photos?query={self.image_query}&per_page={per_page}&page={page}"
        # url = f"https://api.unsplash.com/search/photos?query={self.image_query}&per_page={per_page}"
        headers = {"Authorization": f"Client-ID {self.access_key}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
        else:
            print(f"Error: Received status code {response.status_code}")
            return []

        image_files = []  # List to store the file paths of the images

        if data["results"]:
            for i, result in enumerate(data["results"]):
                print(f"Downloading image {i+1} of {per_page}")
                file_path = 'images/' + self.image_query + '/'
                # Create the directory if it does not exist
                os.makedirs(file_path, exist_ok=True)
                filename = f"{file_path}{self.image_query}_{i}_{self.platform}.jpg"
                temp_filename = f"{file_path}{self.image_query}_{i}_{self.platform}_temp.jpg"
                
                # Download the image
                self.download_image(result["urls"]["full"], temp_filename)
                
                # Resize the downloaded image
                self.resize_image(temp_filename, self.platform, filename)
                
                # Delete the temporary image file
                os.remove(temp_filename)

                # Add the file path of the image to the list
                image_files.append(filename)
        else:
            raise ValueError('No results found for the given query')

        # Return the list of image file paths
        return image_files

    def fetch_video(self):
        pass