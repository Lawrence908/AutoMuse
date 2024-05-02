import json
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import simpledialog, Listbox, Toplevel, Label, Canvas, Frame, Scrollbar, VERTICAL
from automator import Automator

class AutomatorGUI:
    def __init__(self, master):
        self.master = master
        master.title("AutoMuse")
        master.geometry("1200x900")
        master.resizable(False, False)
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        self.automator = Automator()  # Initialize the Automator class
        # Initialize image_selection_frame
        self.image_selection_frame = None

        with open('config/unsplash_queries.json') as f:
            self.unsplash_queries = json.load(f)

        with open('config/platform_dimensions.json') as f:
            data = json.load(f)
        self.platforms = list(data.keys())

        with open('config/quotable_tags.json') as f:
            self.quotable_tags = json.load(f)

        with open('config/fonts.json') as f:
            self.fonts = json.load(f)

        self.platform_combobox = ttk.Combobox(self.master, values=self.platforms)
        self.platform_combobox.pack()
        self.platform_combobox.set(self.platforms[0])

        # Define the image query dropdown menu
        self.label1 = tk.Label(master, text="Image Query:")
        self.query_var = tk.StringVar(master)  # Variable to hold the selected query
        self.query_var.set(self.unsplash_queries[0])  # Default value
        self.query_option_menu = ttk.Combobox(master, textvariable=self.query_var, values=self.unsplash_queries)
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
        self.quote_var.set("Quotable")  # Default value
        self.quote_option_menu = tk.OptionMenu(master, self.quote_var, "Enter your own text", "Quotable", "stoic_quotes.json")

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
        # Destroy the previous image frame if it exists
        if hasattr(self, 'image_frame'):
            self.image_frame.destroy()

        image_query = self.query_var.get()
        self.automator.image_query = image_query
        self.automator.platform = self.platform_combobox.get()
        print("In fetch_image")
        print(f"Fetching images for query: {image_query}")
        print(f"Platform: {self.automator.platform}")
        self.automator.create_media_fetcher()
        self.image_files = self.automator.fetch_media()
        self.display_images()

    def display_images(self):
        if self.image_files is None:
            print("No images to display")
        else:
            # Create a frame for the image thumbnails
            self.image_frame = Frame(self.master, width=1150, height=800)
            self.image_frame.pack_propagate(False)  # Don't shrink the frame to fit its contents
            self.image_frame.pack(side='top', expand=True, fill='both')

            # Create a canvas inside the frame
            self.canvas = Canvas(self.image_frame)
            self.canvas.pack(side='top', fill='both', expand=True)

            # Create a frame inside the canvas to hold the thumbnails
            self.thumbnail_frame = Frame(self.canvas)
            self.canvas.create_window((0, 0), window=self.thumbnail_frame, anchor='nw')

            row, column = 0, 0
            for image_file in self.image_files:
                image = Image.open(image_file)
                if self.automator.platform == 'instagram_story':
                    image.thumbnail((400, 400))
                else:
                    image.thumbnail((200, 200))
                photo = ImageTk.PhotoImage(image)

                # Create the frame
                self.image_selection_frame = tk.Frame(self.master)
                self.image_selection_frame.pack(side='right', fill='both', expand=True)

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



    def fetch_quote(self):
        print("In fetch_quote")  # Debug print

        # # Define platform before assigning it
        # platform = self.platform_combobox.get()
        # self.automator.platform = platform

        # Define text_overlay_option before assigning it
        text_overlay_option = self.overlay_combobox.get()
        self.automator.text_overlay_option = text_overlay_option

        # Define font before assigning it
        font = self.font_combobox.get()
        self.automator.font = font

        # Define quote before assigning it
        quote = self.quote_textbox.get("1.0", 'end')
        self.automator.quote = quote

        # Define author before using it
        author = "Some value"
        self.automator.author = author

        # Define tag before using it
        tag = "Some value"
        self.automator.tag = tag

        quote_option = self.quote_combobox.get()

        self.automator.quote_option = quote_option
        self.automator.text_overlay_option = text_overlay_option
        # self.automator.platform = platform
        self.automator.font = font
        self.automator.tag = tag
        self.automator.quote = quote
        self.automator.author = author

        print("End of fetch_quote")  # Debug print

    def select_image(self, image_file):
        self.selected_image_file = image_file  # Update the selected image file
        print(f"Selected image: {image_file}")  # Debug print
        self.image_file = image_file

        # Hide the image query dropdown and fetch image button
        self.label1.pack_forget()
        self.query_option_menu.pack_forget()
        self.fetch_image_button.pack_forget()

        # Show the selected image
        self.image_frame.destroy()  # Destroy the previous image frame
        self.image_frame = Frame(self.master)  # Create a new frame for the selected image
        self.image_frame.pack(side='left', expand=True, fill='both')

        image = Image.open(self.image_file)
        image.thumbnail((700, 700))
        photo = ImageTk.PhotoImage(image)

        label = Label(self.image_frame, image=photo)
        label.image = photo
        label.pack()

        # Hide the image selection frame and show the quote options frame
        self.image_selection_frame.pack_forget()

        # Show the quote options and fetch quote button
        self.display_quote_options()

        # Fetch the quote based on the selected image
        self.fetch_quote()

    def display_quote_options(self):
        print("In display_quote_options")  # Debug print
        # ... rest of the code ...

        # Hide the platform combobox
        if hasattr(self, 'platform_combobox'):
            self.platform_combobox.pack_forget()

        # Create a new frame for the quote options
        self.quote_options_frame = tk.Frame(self.master)
        self.quote_options_frame.pack(side='right', fill='both', expand=True)

        # Create the quote options dropdown
        self.quote_combobox = ttk.Combobox(self.quote_options_frame, values=[ "Quotable","Enter your own text", "stoic_quotes.json"])
        self.quote_combobox.pack()
        self.quote_combobox.set('Quotable')

        # Add a callback for when the selected quote option changes
        self.quote_combobox.bind('<<ComboboxSelected>>', self.update_quote_options)

        self.overlay_combobox = ttk.Combobox(self.quote_options_frame, values=["Top", "Middle", "Bottom"])
        self.overlay_combobox.pack()
        self.overlay_combobox.set('Middle')

        tag_options = [f"{tag} ({count})" for tag, count in self.quotable_tags.items()]
        self.tag_combobox = ttk.Combobox(self.quote_options_frame, values=tag_options)
        self.tag_combobox.pack()
        self.tag_combobox.set(tag_options[0])

        self.font_combobox = ttk.Combobox(self.quote_options_frame, values=list(self.fonts.keys()))
        self.font_combobox.pack()
        self.font_combobox.set('roboto_bold')

        # Set up the button
        self.process_button = tk.Button(self.quote_options_frame, text="Process Image", command=self.process_image)
        self.process_button.pack()

        # # Add a command to the process button to hide the quote options frame and show the next frame
        # self.process_button.config(command=self.show_next_frame)

        # Create the textboxes for the quote and author, but don't pack them yet
        self.quote_textbox = tk.Text(self.quote_options_frame, height=2, width=30)
        self.author_textbox = tk.Text(self.quote_options_frame, height=2, width=30)

        # Set up the back button
        def back():
            # Clear the current image selection
            self.current_image = None

            # Hide the selected image
            if hasattr(self, 'image_frame'):
                self.image_frame.pack_forget()

            # Hide the quote options frame
            if hasattr(self, 'quote_options_frame'):
                self.quote_options_frame.pack_forget()

            # Show the select images window again
            self.display_select_images_window()

        back_button = tk.Button(self.quote_options_frame, text="Back", command=back)
        back_button.pack()

    def update_quote_options(self, event):
        # Get the selected quote option
        quote_option = self.quote_combobox.get()

        # Only destroy the widgets that need to be replaced
        if hasattr(self, 'quote_label'):
            self.quote_label.destroy()
            del self.quote_label
        if hasattr(self, 'author_label'):
            self.author_label.destroy()
            del self.author_label
        if hasattr(self, 'quote_textbox'):
            self.quote_textbox.destroy()
            del self.quote_textbox
        if hasattr(self, 'author_textbox'):
            self.author_textbox.destroy()
            del self.author_textbox

        # Hide the tag_combobox
        self.tag_combobox.pack_forget()

        if quote_option == 'Enter your own text':
            # Create the quote and author labels and textboxes
            self.quote_label = tk.Label(self.quote_options_frame, text="Quote:")
            self.quote_label.pack()
            self.quote_textbox = tk.Entry(self.quote_options_frame)
            self.quote_textbox.pack()

            self.author_label = tk.Label(self.quote_options_frame, text="Author:")
            self.author_label.pack()
            self.author_textbox = tk.Entry(self.quote_options_frame)
            self.author_textbox.pack()

        elif quote_option == 'Quotable':
            # Show the tag_combobox
            self.tag_combobox.pack()

    def display_select_images_window(self):
        # Pack the platform combobox
        self.platform_combobox.pack()

        # Pack the image query dropdown menu
        self.label1.pack()
        self.query_option_menu.pack()

        # Pack the fetch image button
        self.fetch_image_button.pack()

        # Call the method to display the images
        self.display_images()

    def show_next_frame(self):
        # Define next_frame before packing it
        self.next_frame = tk.Frame(self.master)
        self.next_frame.pack(side='right', fill='both', expand=True)

    def process_image(self):
        print("In process_image")
        # Get the selected options
        quote_option = self.quote_combobox.get()
        print("quote_option:", quote_option)
        overlay_option = self.overlay_combobox.get()
        print("overlay_option:", overlay_option)
        # platform_option = self.platform_combobox.get()
        # print("platform_option:", platform_option)
        tag_option = self.tag_combobox.get()
        print("tag_option:", tag_option)
        tag = tag_option.split()[0]  # Extract the tag from the selected option
        print("tag:", tag)
        font_option = self.font_combobox.get()
        print("font_option:", font_option)

        if quote_option == "Enter your own text":
            quote = self.quote_textbox.get()
            author = self.author_textbox.get()

        else:
            quote = None
            author = None

        print("End of process_image")

        print("author:", author)
        print("quote:", quote)

        # Process the image with the selected options
        print("Setting parameters...")
        self.automator.set_parameters(self.query_var.get(), quote_option, overlay_option, self.automator.platform, tag, quote, author, font_option)
        print("Parameters set")
        print("Fetching quote and processing media...")
        self.automator.fetch_quote_and_process_media(self.image_file)

        print("Image processed")



if __name__ == "__main__":
    root = tk.Tk()
    gui = AutomatorGUI(root)
    root.mainloop()