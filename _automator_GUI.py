import json
import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
from automator import Automator

class AutomatorGUI:
    def __init__(self, master):
        self.master = master
        master.title("AutoMuse")
        master.geometry("500x300")

        self.automator = Automator(...)
        self.fetch_media_button = tk.Button(master, text="Fetch Media", command=self.automator.fetch_media)
        self.fetch_quote_and_process_media_button = tk.Button(master, text="Fetch Quote and Process Media", command=self.automator.fetch_quote_and_process_media)

        # Load the platform dimensions from the JSON file
        with open('config/platform_dimensions.json') as f:
            data = json.load(f)
        self.platforms = list(data.keys())

        with open('config/quotable_tags.json') as f:
            data = json.load(f)
        self.quotable_tags = {item[0]: item[1] for item in data}

        self.label1 = tk.Label(master, text="Enter an image query:")
        self.label1.pack()

        self.entry1 = tk.Entry(master)
        self.entry1.pack()

        self.label2 = tk.Label(master, text="Choose a quote option:")
        self.label2.pack()

        self.quote_var = tk.StringVar(master)
        self.quote_var.set("stoic_quotes.json") # default value

        self.quote_option_menu = tk.OptionMenu(master, self.quote_var, "stoic_quotes.json", "quotable", "Enter your own text")
        self.quote_option_menu.pack()

        self.label3 = tk.Label(master, text="Choose a text overlay option:")
        self.label3.pack()

        self.overlay_var = tk.StringVar(master)
        self.overlay_var.set("Top") # default value

        self.overlay_option_menu = tk.OptionMenu(master, self.overlay_var, "Top", "Middle", "Bottom")
        self.overlay_option_menu.pack()

        self.label4 = tk.Label(master, text="Choose a platform:")
        self.label4.pack()

        self.label5 = tk.Label(master, text="Choose a quotable tag:")
        self.label5.pack()

        self.tag_var = tk.StringVar(master)
        self.tag_var.set(list(self.quotable_tags.keys())[0]) # default value

        self.tag_option_menu = tk.OptionMenu(master, self.tag_var, *self.quotable_tags)
        self.tag_option_menu.pack()

        # Load the available fonts from the JSON file
        with open('config/fonts.json') as f:
            self.fonts = json.load(f)
        self.available_fonts = list(self.fonts.keys())

        self.label6 = tk.Label(master, text="Choose a font:")
        self.label6.pack()

        self.font_var = tk.StringVar(master)
        self.font_var.set(self.available_fonts[0]) # default value

        self.font_option_menu = tk.OptionMenu(master, self.font_var, *self.available_fonts)
        self.font_option_menu.pack()

        self.platform_var = tk.StringVar(master)
        self.platform_var.set(self.platforms[0]) # default value

        self.platform_option_menu = tk.OptionMenu(master, self.platform_var, *self.platforms)
        self.platform_option_menu.pack()

        self.fetch_button = tk.Button(master, text="Fetch and Process", command=self.fetch_and_process)
        self.fetch_button.pack()

    def fetch_image(self):
        image_query = self.entry1.get()
        self.automator.image_query = image_query
        self.automator.fetch_media()
        self.display_image()

    def fetch_quote_and_process(self):
        quote_option = self.quote_var.get()
        text_overlay_option = self.overlay_var.get()
        platform = self.platform_var.get()
        font = self.font_var.get()
        tag = None
        quote = None
        author = None

        if quote_option == "Enter your own text":
            quote = simpledialog.askstring("Input", "Enter your quote:")
            author = simpledialog.askstring("Input", "Enter the author:")
        elif quote_option == "quotable":
            tag = self.tag_var.get()

        self.automator.quote_option = quote_option
        self.automator.text_overlay_option = text_overlay_option
        self.automator.platform = platform
        self.automator.font = font
        self.automator.tag = tag
        self.automator.quote = quote
        self.automator.author = author

        self.automator.fetch_quote_and_process_media()

    def display_image(self):
        # Use PIL to open the image and convert it to a format that can be used in Tkinter
        image = Image.open(self.automator.media)
        photo = ImageTk.PhotoImage(image)

        # Create a label and add the image to it
        image_label = tk.Label(self.master, image=photo)
        image_label.image = photo  # Keep a reference to the image to prevent it from being garbage collected
        image_label.pack()

root = tk.Tk()
gui = AutomatorGUI(root)
root.mainloop()