import unittest
from unittest.mock import patch, MagicMock
from quote_fetcher import QuoteFetcher

class TestQuoteFetcher(unittest.TestCase):
    def setUp(self):
        self.fetcher = QuoteFetcher()

    @patch('builtins.open', new_callable=MagicMock)
    @patch('json.load')
    @patch('random.choice')
    def test_fetch_quote(self, mock_choice, mock_load, mock_open):
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        mock_load.return_value = [
            {"quote": "The best revenge is not to be like your enemy.", "author": "Marcus Aurelius"},
            {"quote": "It's not what happens to you, but how you react to it that matters.", "author": "Epictetus"}
        ]
        mock_choice.return_value = {"quote": "The best revenge is not to be like your enemy.", "author": "Marcus Aurelius"}

        result = self.fetcher.fetch_quote('dummy_path')
        expected = '"The best revenge is not to be like your enemy."\n - Marcus Aurelius'
        self.assertEqual(result, expected)

    @patch('requests.get')
    def test_fetch_quote_from_api(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"content": "The best revenge is not to be like your enemy.", "author": "Marcus Aurelius"}
        mock_get.return_value = mock_response

        result = self.fetcher.fetch_quote_from_api('stoicism')
        expected = '"The best revenge is not to be like your enemy."\n - Marcus Aurelius'
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()