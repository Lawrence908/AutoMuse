import json
from media_fetcher import MediaFetcher
from quote_fetcher import QuoteFetcher
from media_processor import MediaProcessor

class Automator:
    def __init__(self):
        self.image_query = None
        self.quote_option = None
        self.text_overlay_option = None
        self.platform = None
        self.tag = None
        self.quote = None
        self.author = None
        self.font = 'roboto_bold'
        self.media = None

        self.media_fetcher = None
        self.quote_fetcher = None
        self.media_processor = MediaProcessor()

    def create_media_fetcher(self):
        self.media_fetcher = MediaFetcher(self.image_query, self.platform)

    def set_parameters(self, image_query, quote_option, text_overlay_option, platform, tag=None, quote=None, author=None, font='roboto_bold'):
        self.image_query = image_query
        self.quote_option = quote_option
        self.text_overlay_option = text_overlay_option
        self.platform = platform
        self.tag = tag
        self.quote = quote
        self.author = author
        self.font = font

        self.media_fetcher = MediaFetcher(self.image_query, self.platform)
        self.quote_fetcher = QuoteFetcher(self.quote_option, self.tag, quote, author)

    def fetch_media(self):
        self.media_files = self.media_fetcher.fetch_image()
        return self.media_files
    
    def fetch_quote_and_process_media(self):
        quote = self.quote_fetcher.fetch_quote()
        self.media_processor.process_media(media_type='image', path=self.media, platform=self.platform, quote=self.quote, text_overlay_option=self.text_overlay_option, font=self.font)