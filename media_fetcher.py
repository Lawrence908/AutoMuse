import os
import requests
from PIL import Image
import io

class MediaFetcher:
    def __init__(self, access_key):
        self.access_key = os.getenv("UNSPLASH_ACCESS_KEY")
        self.platform_dimensions = {
            'facebook': ((1, 1), 1080),  # aspect ratio and max dimension for Facebook
            'twitter': ((16, 9), 1024),  # aspect ratio and max dimension for Twitter
            'instagram': ((1, 1), 1080)  # aspect ratio and max dimension for Instagram
        }
        self.query_history = []

    def download_image(self, image_url, filename):
        # Download the image
        response = requests.get(image_url)
        image = Image.open(io.BytesIO(response.content))
        
        # Save the image
        image.save(filename)

    def resize_image(self, image_path, platform, aspect_ratio, max_dimension, filename):
        # Open the image
        image = Image.open(image_path)

        # Get the aspect ratio and max dimension for the platform
        aspect_ratio, max_dimension = self.platform_dimensions.get(platform)
        if aspect_ratio and max_dimension:
            # Calculate the aspect ratio of the image and the target size
            image_aspect_ratio = image.width / image.height
            target_aspect_ratio = aspect_ratio[0] / aspect_ratio[1]

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
            scaling_factor = max_dimension / max(image.width, image.height)

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

    def fetch_image(self, query="nature", per_page=10):
        # If the query is in history, skip the download
        if query in self.query_history:
            return []

        # Add the query to the history
        self.query_history.append(query)

        url = f"https://api.unsplash.com/search/photos?query={query}&per_page={per_page}"
        headers = {"Authorization": f"Client-ID {self.access_key}"}
        response = requests.get(url, headers=headers)
        data = response.json()

        # The API returns a list of photos. Let's return all of them.
        if data["results"]:
            for i, result in enumerate(data["results"]):
                # for platform in self.platform_dimensions:
                for platform, (aspect_ratio, max_dimension) in self.platform_dimensions.items():
                    file_path = 'tests/test_files/'
                    filename = f"{file_path}{query}_{i}_{platform}.jpg"
                    temp_filename = f"{file_path}{query}_{i}_{platform}_temp.jpg"
                    
                    # Download the image
                    self.download_image(result["urls"]["full"], temp_filename)
                    
                    # Resize the downloaded image
                    # self.resize_image(temp_filename, platform, filename)
                    self.resize_image(temp_filename, platform, aspect_ratio, max_dimension, filename)
                    
                    # Delete the temporary image file
                    os.remove(temp_filename)
        else:
            return []

    def fetch_video(self):
        pass