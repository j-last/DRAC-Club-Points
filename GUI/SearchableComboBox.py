
import customtkinter as ctk

class SearchableComboBox(ctk.CTkComboBox):
    """A CTkComboBox whose options can be searched through.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<KeyRelease>", self.search_options)
        self.options = kwargs["values"]

    def set_options(self, options:list):
        """Sets the values of the combobox to the new values/options.
        """
        self.options = options
        self.configure(values=options)
    
    def search_options(self, event):
        """Updates the dropdown options based on what has been typed so far, and opens the dropdown.

        Bug: Unfortunately the dropdown cannot be open whilst you type, so after 1 letter the dropdown
        menu opens and you have to reselect the text box.
        """
        text = self.get()

        if text == "":
            options = self.options
        else:
            num_chars = len(text)
            options = [item for item in self.options if item.lower()[:num_chars] == text.lower()]

        self.configure(values=options)
        self._open_dropdown_menu()

