import json
from media_fetcher import MediaFetcher
from quote_fetcher import QuoteFetcher
from media_processor import MediaProcessor
from text_to_speech import TextToSpeech
from social_media_poster import SocialMediaPoster

class Automator:
    def __init__(self, config_file):
        with open(config_file) as f:
            config = json.load(f)

        self.channel = config["channel"]
        self.media_source = config["media_source"]
        self.text_source = config["text_source"]
        self.post_frequency = config["post_frequency"]
        
        self.media_fetcher = MediaFetcher()
        self.quote_fetcher = QuoteFetcher()
        self.media_processor = MediaProcessor()
        self.text_to_speech = TextToSpeech()
        self.social_media_poster = SocialMediaPoster()

    def automate(self):
        pass