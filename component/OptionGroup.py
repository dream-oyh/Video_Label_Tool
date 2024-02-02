import tkinter as tk


class OptionGroup(tk.Frame):
    def __init__(self, option: list, **kwargs):
        super().__init__(**kwargs)
        self.num = tk.IntVar()
        self.num.set(0)
        for i, o in enumerate(option):
            b = tk.Radiobutton(self, text=o, variable=self.num, value=i)
            b.grid(row=i, column=0, sticky="w")
            
            
