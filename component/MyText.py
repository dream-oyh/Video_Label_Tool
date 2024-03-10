import customtkinter as tk


class TextRedirector:
    def __init__(self, widget, tag="stdout", **kwargs):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert(tk.END, str, (self.tag,))
        self.widget.see(tk.END)
        self.widget.configure(state="disabled")

    def flush(self):
        pass
