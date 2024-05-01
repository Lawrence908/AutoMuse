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