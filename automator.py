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
        print("In create_media_fetcher")
        print("self.image_query", self.image_query)
        print("self.platform", self.platform)
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
        print("End of set_parameters")

    def fetch_media(self):
        print("fetch_media")
        print("self.platform", self.platform)
        self.media_files = self.media_fetcher.fetch_image(self.platform)
        return self.media_files
    
    def fetch_quote(self):
        if self.quote_option == "Enter your own text":
            self.quote = self.quote_fetcher.user_entered_quote(self.quote, self.author)
        elif self.quote_option == "Quotable":
            self.quote = self.quote_fetcher.fetch_quote_from_api(self.tag)

        ### Edit later to make modular for different quote files ###
        elif self.quote_option == "stoic_quotes.json":
            self.quote = self.quote_fetcher.fetch_quote(file_path='quotes/stoic_quotes.json')
            # self.quote = QuoteFetcher(quote_option=self.quote_option, tag=self.tag, quote=self.quote, author=self.author)
        ## Insert new quote files here as above ##

        else:
            raise ValueError("Invalid quote option")
        return self.quote
    
    def process_media(self, media_file):
        if media_file:
            self.media = media_file
        
        print ("Automator process_media")
        print ("self.text_overlay_option", self.text_overlay_option)
        print ("self.quote", self.quote)
        print ("self.platform", self.platform)
        print ("self.font", self.font)
        print ("self.quote_option", self.quote_option)
        print ("self.media", self.media)

        return self.media_processor.process_media(media_type='image', path=self.media, text=self.quote, platform=self.platform, text_overlay_option=self.text_overlay_option, font=self.font)