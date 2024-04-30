import unittest
from PIL import Image
from media_processor import MediaProcessor

class TestMediaProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = MediaProcessor()

    def test_overlay_text_on_image(self):
        image = Image.new('RGB', (100, 100))
        text = 'Test'
        platform = 'facebook'
        processed_image = self.processor.overlay_text_on_image(image, text, platform)
        font_size = self.processor.estimate_font_size(image, text, self.processor.fonts.get('ubuntu'), self.processor.font_size_ratio)
        print(f'Font size: {font_size}')  # Print the font size
        self.assertGreater(font_size, 0)  # Assert that font size is greater than 0
        self.assertEqual(processed_image.size, self.processor.platform_dimensions[platform])

    # def test_overlay_text_on_video(self):
    #     video_path = 'tests/test_files/test_video.mp4'  # Replace with path to a test video
    #     text = 'Test'
    #     platform = 'facebook'
    #     processed_video = self.processor.overlay_text_on_video(video_path, text, platform)
    #     self.assertEqual(processed_video.size, self.processor.platform_dimensions[platform])

    # def test_add_voice_over(self):
    #     video_path = 'tests/test_files/test_video.mp4'  # Replace with path to a test video
    #     audio_folder = 'test_audio'  # Replace with path to a folder with test audio files
    #     processed_video = self.processor.add_voice_over(video_path, audio_folder)
    #     self.assertIsNotNone(processed_video.audio)

    def test_process_media(self):
        image_path = 'tests/test_files/test_image_0.jpg'  # Replace with path to a test image
        text = 'Test'
        platform = 'facebook'
        processed_image_path = 'tests/test_files/processed_image0.jpg'
        self.processor.process_media('image', image_path, platform, output_file=processed_image_path, quote_file='quotes/stoic_quotes.json')
        font_size = self.processor.estimate_font_size(Image.open(image_path), text, self.processor.fonts.get('ubuntu'), self.processor.font_size_ratio)
        # print(f'Font size: {font_size}')  # Print the font size
        self.assertGreater(font_size, 0)  # Assert that font size is greater than 0
        self.assertTrue(os.path.exists(processed_image_path))

if __name__ == '__main__':
    unittest.main()