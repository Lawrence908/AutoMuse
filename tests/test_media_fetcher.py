import unittest
from unittest.mock import patch
from media_fetcher import MediaFetcher

class TestMediaFetcher(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_image(self, mock_get):
        # Mock the response from the Unsplash API
        mock_get.return_value.json.return_value = {
            "results": [
                {
                    "urls": {
                        "full": "https://example.com/image.jpg"
                    }
                }
            ]
        }

        mock_access_key = "mock_access_key"
        fetcher = MediaFetcher(mock_access_key)
        image_url = fetcher.fetch_image()

        self.assertEqual(image_url, "https://example.com/image.jpg")

if __name__ == '__main__':
    unittest.main()