import customtkinter as tk


class MySlider(tk.CTkFrame):
    def __init__(self, master, text, state, min=0, max=10, solution=10, **kwargs):
        super().__init__(master,  **kwargs)
        self.label = tk.CTkLabel(master=self, text=text)
        # self.label.grid(row=0, column=0)
        self.x = tk.IntVar(value=0)
        self.slider = tk.CTkSlider(
            master=self, from_=min, to=max, number_of_steps=solution, variable=self.x, state=state
        )
        self.entry = tk.CTkEntry(master=self, textvariable=self.x)
        self.label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.slider.grid(row=1, column=0, padx=5, pady=5)
        self.entry.grid(row=1, column=1, padx=5, pady=5)
