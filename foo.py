from tkinter import ttk

class AutomatorGUI:
    # ...

    def display_quote_options(self):
        # Create a combobox for each option
        self.quote_combobox = ttk.Combobox(self.master, values=["Enter your own text", "quotable", "stoic_quotes.json"])
        self.quote_combobox.pack()
        self.quote_combobox.set('Enter your own text')

        self.overlay_combobox = ttk.Combobox(self.master, values=["Top", "Middle", "Bottom"])
        self.overlay_combobox.pack()
        self.overlay_combobox.set('Top')

        self.platform_combobox = ttk.Combobox(self.master, values=self.platforms)
        self.platform_combobox.pack()
        self.platform_combobox.set(self.platforms[0])

        tag_options = [f"{tag} ({count})" for tag, count in self.quotable_tags.items()]
        self.tag_combobox = ttk.Combobox(self.master, values=tag_options)
        self.tag_combobox.pack()
        self.tag_combobox.set(tag_options[0])

        self.font_combobox = ttk.Combobox(self.master, values=list(self.fonts.keys()))
        self.font_combobox.pack()
        self.font_combobox.set('roboto_bold')

        # Add a button to process the image after selecting the options
        self.process_button = tk.Button(self.master, text="Process Image", command=self.process_image)
        self.process_button.pack()

    def process_image(self):
        # Get the selected options
        quote_option = self.quote_combobox.get()
        overlay_option = self.overlay_combobox.get()
        platform_option = self.platform_combobox.get()
        tag_option = self.tag_combobox.get()
        font_option = self.font_combobox.get()

        # Process the image with the selected options