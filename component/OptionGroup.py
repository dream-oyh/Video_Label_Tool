import customtkinter as tk


class OptionGroup(tk.CTkFrame):
    def __init__(self, option: list, master, state, default=1,  **kwargs):
        super().__init__(master, **kwargs)
        self.num = tk.IntVar()
        self.num.set(default - 1 )
        for i, o in enumerate(option):
            b = tk.CTkRadioButton(self, text=o, variable=self.num, value=i, state=state)
            b.grid(row=i, column=0, sticky="w", pady=10)
