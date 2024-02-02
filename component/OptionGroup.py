import customtkinter as tk


class OptionGroup(tk.CTkFrame):
    def __init__(self, option: list, master, **kwargs):
        super().__init__(master, **kwargs)
        self.num = tk.IntVar()
        self.num.set(0)
        for i, o in enumerate(option):
            b = tk.CTkRadioButton(self, text=o, variable=self.num, value=i)
            b.grid(row=i, column=0, sticky="w")
