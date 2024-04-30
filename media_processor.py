import os
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
from quote_fetcher import QuoteFetcher

class MediaProcessor:
    def __init__(self):
        self.platform_dimensions = {
            'facebook': (1.91, 1),
            'twitter': (2, 1),
            'instagram': (1, 1)
        }
        self.fonts = {
            'jersey': "fonts/Jersey_15/Jersey15-Regular.ttf",
            'monsterat': "fonts/Montserrat/static/Montserrat-Regular.ttf",
            'playfair': 'fonts/Playfair_Display/static/PlayfairDisplay-Regular.ttf',
            'roboto': 'fonts/Roboto/Roboto-Regular.ttf',
            'roboto_bold': 'fonts/Roboto/Roboto-BoldItalic.ttf',
            'roboto_mono': 'fonts/Roboto_Mono/static/RobotoMono-Regular.ttf',
            'ubuntu': 'fonts/Ubuntu/Ubuntu-Regular.ttf'
        }

    def overlay_text_on_image(self, image, text, platform, font='ubuntu', font_size_ratio=0.05, padding_ratio=0.01, corner_radius_ratio=0.02):
        dimensions = self.platform_dimensions.get(platform)
        if dimensions:
            # Resize image to dimensions
            image = image.resize((int(image.width * dimensions[0]), int(image.height * dimensions[1])))
        # Overlay text on image
        draw = ImageDraw.Draw(image)
        font_file = self.fonts.get(font)
        if not font_file:
            font_file = self.fonts.get('ubuntu')
        if font_file:
            # Estimate font size based on image size and text length
            font_size = self.estimate_font_size(image, text, font_file, font_size_ratio)
            font = ImageFont.truetype(font_file, font_size)
            # Estimate the size of the text
            lines = text.split('\n')
            max_text_width = max(draw.textlength(line, font=font) for line in lines)
            text_height = font_size * len(lines)  # The height of the text is roughly the size of the font times the number of lines
            # Calculate position to center text
            x = (image.width - max_text_width) / 2
            y = (image.height - text_height) / 2
            # Calculate padding and corner radius
            padding = max(image.width, image.height) * padding_ratio
            corner_radius = max(image.width, image.height) * corner_radius_ratio
            # Draw semi-transparent box
            box_color = (0, 0, 0, 128)  # Replace (0, 0, 0, 128) with the desired box color and transparency
            box_image = Image.new('RGBA', image.size, (0, 0, 0, 0))
            box_draw = ImageDraw.Draw(box_image)
            box_draw.rounded_rectangle([x - padding, y - padding, x + max_text_width + padding, y + text_height + padding], fill=box_color, radius=corner_radius)
            image = Image.alpha_composite(image.convert('RGBA'), box_image)
            draw = ImageDraw.Draw(image)
            # Draw text with drop shadow
            shadow_color = "black"
            shadow_offset = 2
            draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=shadow_color)
            draw.text((x, y), text, font=font, fill=(255, 255, 255))  # Replace (255, 255, 255) with the desired text color
        # Convert image to RGB mode before saving
        return image.convert('RGB')

    def estimate_font_size(self, image, text, font_file, font_size_ratio):
        # Start with a font size proportional to image width
        font_size = int(font_size_ratio * image.width)
        font_size = min(font_size, 45)  # Add an upper limit to the initial font size
        font = ImageFont.truetype(font_file, max(font_size, 70))  # Ensure font_size is at least 50
        # Create off-screen image and draw text
        offscreen = Image.new('RGB', (1, 1))
        offscreen_draw = ImageDraw.Draw(offscreen)
        # Split text into lines
        lines = text.split('\n')
        # Get maximum width of lines
        max_text_width = max(offscreen_draw.textlength(line, font=font) for line in lines)
        # If max text width is greater than image width, reduce font size
        while max_text_width > image.width:
            font_size -= 1
            font_size = max(font_size, 1)  # Ensure font_size is at least 1
            font = ImageFont.truetype(font_file, font_size)
            max_text_width = max(offscreen_draw.textlength(line, font=font) for line in lines)
        return font_size


    def overlay_text_on_video(self, video_path, text, platform, font='ubuntu', font_size=24):
        dimensions = self.platform_dimensions.get(platform)
        font_file = self.fonts.get(font)
        if not font_file:
            font_file = self.fonts.get('ubuntu')  # Use 'ubuntu' as the default font

        # Load the video
        video = VideoFileClip(video_path)

        if dimensions:
            video = video.resize(dimensions)

        # Create a TextClip for each line of text
        text_clips = [TextClip(txt, fontsize=font_size, font=font_file, color='white') for txt in text.split('\n')]

        # Position the text clips in the center of the video
        text_clips = [txt.set_position('center').set_duration(video.duration) for txt in text_clips]

        # Overlay the text clips on the video
        video = CompositeVideoClip([video] + text_clips)

        return video
    
    def add_voice_over(self, video_path, audio_folder):
        # Load the video
        video = VideoFileClip(video_path)

        # Get the duration of the video
        video_duration = video.duration

        # Get a list of all audio files in the audio folder
        audio_files = os.listdir(audio_folder)

        # Filter the audio files based on their duration
        suitable_audio_files = [audio for audio in audio_files if AudioFileClip(os.path.join(audio_folder, audio)).duration < video_duration]

        # If there are suitable audio files, select one and add it to the video
        if suitable_audio_files:
            audio_path = os.path.join(audio_folder, suitable_audio_files[0])
            audio = AudioFileClip(audio_path)
            video = video.set_audio(audio)

        return video
    def process_media(self, media_type, path, platform, font='roboto_bold', font_size_ratio=0.05, audio_folder=None, output_file=None, quote_file=None, quote_topic=None, quote=None):
        # Instantiate the QuoteFetcher class
        quote_fetcher = QuoteFetcher()

        # Fetch a quote
        if quote_file:
            text = quote_fetcher.fetch_quote(quote_file)
        elif quote_topic:
            text = quote_fetcher.fetch_quote_from_api(quote_topic)
        elif quote:
            text = quote
        else:
            raise ValueError('Either quote_file, quote_topic, or quote must be provided')

        if media_type == 'image':
            image = Image.open(path)
            processed_image = self.overlay_text_on_image(image, text, platform, font, font_size_ratio)
            output_file = output_file if output_file else 'processed_image.jpg'
            processed_image.save(output_file)
        elif media_type == 'video':
            processed_video = self.overlay_text_on_video(path, text, platform, font, font_size_ratio)
            if audio_folder:
                processed_video = self.add_voice_over(processed_video, audio_folder)
            output_file = output_file if output_file else 'processed_video.mp4'
            processed_video.write_videofile(output_file, codec='libx264')
        else:
            raise ValueError('Unsupported media type')