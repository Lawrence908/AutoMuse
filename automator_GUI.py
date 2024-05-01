import json
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import simpledialog, Listbox, Toplevel, Label, Canvas, Frame, Scrollbar, VERTICAL
from automator import Automator

class AutomatorGUI:
    def __init__(self, master):
        self.master = master
        master.title("AutoMuse")
        master.geometry("800x600")

        self.automator = Automator()  # Initialize the Automator class

        with open('config/unsplash_queries.json') as f:
            self.unsplash_queries = json.load(f)

        with open('config/platform_dimensions.json') as f:
            data = json.load(f)
        self.platforms = list(data.keys())

        with open('config/quotable_tags.json') as f:
            self.quotable_tags = json.load(f)

        with open('config/fonts.json') as f:
            self.fonts = json.load(f)


        # Define the image query dropdown menu
        self.label1 = tk.Label(master, text="Image Query:")
        self.query_var = tk.StringVar(master)  # Variable to hold the selected query
        self.query_var.set(self.unsplash_queries[0])  # Default value
        self.query_option_menu = tk.OptionMenu(master, self.query_var, *self.unsplash_queries)
        self.label1.pack()
        self.query_option_menu.pack()

        # Define the fetch image button
        self.fetch_image_button = tk.Button(master, text="Fetch Image", command=self.fetch_image)
        self.fetch_image_button.pack()

        # Define the fetch quote and process button
        self.fetch_quote_button = tk.Button(master, text="Fetch Quote", command=self.fetch_quote)
        # Define the image query entry widget
        self.label2 = tk.Label(master, text="Quote Option:")
        self.quote_var = tk.StringVar(master)
        self.quote_var.set("Enter your own text")  # Default value
        self.quote_option_menu = tk.OptionMenu(master, self.quote_var, "Enter your own text", "quotable", "stoic_quotes.json")

        # Define the text overlay option widgets
        self.label3 = tk.Label(master, text="Text Overlay Option:")
        self.overlay_var = tk.StringVar(master)
        self.overlay_var.set("Top")  # Default value
        self.overlay_option_menu = tk.OptionMenu(master, self.overlay_var, "Top", "Middle", "Bottom")

        # Define the platform-related widgets
        self.label4 = tk.Label(master, text="Platform:")
        self.platform_var = tk.StringVar(master)
        self.platform_var.set(self.platforms[0])  # Default value
        self.platform_option_menu = tk.OptionMenu(master, self.platform_var, *self.platforms)
        self.label5 = tk.Label(master, text="Tag:")
        self.tag_var = tk.StringVar(master)

        # Assuming self.quotable_tags is the dictionary containing the tags and their counts
        tag_options = [f"{tag} ({count})" for tag, count in self.quotable_tags.items()]
        self.tag_var.set(tag_options[0])  # Default value
        self.tag_option_menu = tk.OptionMenu(master, self.tag_var, *tag_options)

        # Define the font-related widgets
        self.label6 = tk.Label(master, text="Font:")
        self.font_var = tk.StringVar(master)
        self.font_var.set("roboto_bold")  # Default value
        self.font_option_menu = tk.OptionMenu(master, self.font_var, *self.fonts.keys())

        # Hide the other widgets initially
        self.fetch_quote_button.pack_forget()
        self.label2.pack_forget()
        self.quote_option_menu.pack_forget()
        self.label3.pack_forget()
        self.overlay_option_menu.pack_forget()
        self.label4.pack_forget()
        self.platform_option_menu.pack_forget()
        self.label5.pack_forget()
        self.tag_option_menu.pack_forget()
        self.label6.pack_forget()
        self.font_option_menu.pack_forget()

    def fetch_image(self):
        image_query = self.query_var.get()
        self.automator.image_query = image_query
        self.automator.platform = self.platform_var.get()
        self.automator.create_media_fetcher()
        self.image_files = self.automator.fetch_media()
        self.display_images()

    def display_images(self):
        if self.image_files is None:
            print("No images to display")
        else:
            # Create a frame for the image thumbnails
            self.image_frame = Frame(self.master)
            self.image_frame.pack(side='left', expand=True, fill='both')

            # Create a canvas inside the frame
            self.canvas = Canvas(self.image_frame)
            self.canvas.pack(side='left', fill='both', expand=True)

            # Create a frame inside the canvas to hold the thumbnails
            self.thumbnail_frame = Frame(self.canvas)
            self.canvas.create_window((0, 0), window=self.thumbnail_frame, anchor='nw')

            row, column = 0, 0
            for image_file in self.image_files:
                image = Image.open(image_file)
                image.thumbnail((200, 200))
                photo = ImageTk.PhotoImage(image)

                label = Label(self.thumbnail_frame, image=photo)
                label.image = photo
                label.bind('<Button-1>', lambda event, image_file=image_file: self.select_image(image_file))  # Bind click event


                label.grid(row=row, column=column)

                # Update row and column for the next thumbnail
                column += 1
                if column > 4:  # Change this value to adjust the number of thumbnails per row
                    column = 0
                    row += 1

            # Update the scroll region of the canvas after adding the thumbnails
            self.canvas.configure(scrollregion=self.canvas.bbox('all'))

            # Add a button to process all images
            self.process_all_button = tk.Button(self.master, text="Process All Images", command=self.process_all_images)
            self.process_all_button.pack()

        # Show the other widgets in the widget frame
        self.fetch_quote_button.pack(in_=self.widget_frame)
        self.label2.pack(in_=self.widget_frame)
        self.quote_option_menu.pack(in_=self.widget_frame)
        self.label3.pack(in_=self.widget_frame)
        self.overlay_option_menu.pack(in_=self.widget_frame)
        self.label4.pack(in_=self.widget_frame)
        self.platform_option_menu.pack(in_=self.widget_frame)
        self.label5.pack(in_=self.widget_frame)
        self.tag_option_menu.pack(in_=self.widget_frame)
        self.label6.pack(in_=self.widget_frame)
        self.font_option_menu.pack(in_=self.widget_frame)

    def fetch_quote(self):
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
            self.label5.pack_forget()
            self.tag_option_menu.pack_forget()
        elif quote_option == "quotable":
            tag = self.tag_var.get()
            self.label5.pack()
            self.tag_option_menu.pack()
        else:
            self.label5.pack_forget()
            self.tag_option_menu.pack_forget()

        self.automator.quote_option = quote_option
        self.automator.text_overlay_option = text_overlay_option
        self.automator.platform = platform
        self.automator.font = font
        self.automator.tag = tag
        self.automator.quote = quote
        self.automator.author = author

    def select_image(self, image_file):
        self.selected_image_file = image_file  # Update the selected image file
        print(f"Selected image: {image_file}")
        self.fetch_quote() # Fetch the quote based on the selected image

    def display_quote_options(self):
        # Define your quote options
        self.quote_options = ['Option 1', 'Option 2', 'Option 3']

        # Create a dictionary to store the state of each option
        self.quote_options_state = {option: tk.BooleanVar() for option in self.quote_options}

        # Create a checkbox for each option
        for option in self.quote_options:
            checkbox = tk.Checkbutton(self.master, text=option, variable=self.quote_options_state[option])
            checkbox.pack()

        # Add a button to process the image after selecting the options
        self.process_button = tk.Button(self.master, text="Process Image", command=self.process_image)
        self.process_button.pack()

    def process_image(self):
        # Get the selected options
        selected_options = [option for option, state in self.quote_options_state.items() if state.get()]

        print(f"Processing image: {self.selected_image_file} with options: {selected_options}")
        # Add your image processing code here
        # You can access the selected image file with self.selected_image_file
        # You can access the selected options with selected_options

    def process_all_images(self):
        for image_file in self.image_files:
            self.selected_image_file = image_file
            self.fetch_quote()
            self.process_image()



if __name__ == "__main__":
    root = tk.Tk()
    gui = AutomatorGUI(root)
    root.mainloop()