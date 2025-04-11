import tkinter as tk
import customtkinter as ctk
from tkinter import ttk

class TemperatureApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Temperature Gauges")
        self.geometry("600x400")

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.temperatures = [0, 0, 0]
        self.gauges = []
        self.create_gauges()
        self.create_buttons()

    def create_gauges(self):
        for i in range(3):
            frame = ctk.CTkFrame(self)
            frame.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")

            gauge = ttk.Progressbar(frame, orient="vertical", length=200, mode="determinate")
            gauge.pack(pady=10)

            label = ctk.CTkLabel(frame, text=f"{self.temperatures[i]}°C")
            label.pack()

            self.gauges.append((gauge, label))

    def create_buttons(self):
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        buttons = [
            ("Increase All", self.increase_all),
            ("Decrease All", self.decrease_all),
            ("Reset", self.reset),
            ("Quit", self.quit)
        ]

        for i, (text, command) in enumerate(buttons):
            button = ctk.CTkButton(button_frame, text=text, command=command)
            button.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")

        button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

    def update_gauges(self):
        for i, (gauge, label) in enumerate(self.gauges):
            gauge["value"] = self.temperatures[i]
            label.configure(text=f"{self.temperatures[i]}°C")

    def increase_all(self):
        self.temperatures = [t + 5 for t in self.temperatures]
        self.update_gauges()

    def decrease_all(self):
        self.temperatures = [max(t - 5, 0) for t in self.temperatures]
        self.update_gauges()

    def reset(self):
        self.temperatures = [0, 0, 0]
        self.update_gauges()

if __name__ == "__main__":
    app = TemperatureApp()
    app.mainloop()





