import customtkinter as ctk
import tkinter as tk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Application Configuration for 5" Touchscreen
        self.title("Bioreactor UI")
        self.geometry("800x480")  # 5-inch touchscreen resolution
        self.resizable(False, False)  # Fixed size

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.frames = {}
        self.current_frame = None
        self._create_navigation()
        self._create_frames()

    def _create_navigation(self):
        nav_frame = ctk.CTkFrame(self, width=150)
        nav_frame.pack(side="left", fill="y")

        buttons = [
            ("pH", "pHFrame"),
            ("Dissolved O₂", "DOFrame"),
            ("Optical Density", "ODFrame"),
            ("Temperature", "TempFrame"),
            ("Stirring", "StirringFrame"),
            ("Flow", "FlowFrame"),
        ]

        for text, frame_name in buttons:
            ctk.CTkButton(
                nav_frame,
                text=text,
                command=lambda name=frame_name: self.show_frame(name),
                height=70,
                font=("Roboto", 18),
                border_width=2,
                corner_radius=10,
                fg_color="#E0E0E0",
                text_color="black",
                border_color="#4A4A4A"
            ).pack(fill="x")

    def _create_frames(self):
        container = ctk.CTkFrame(self)
        container.pack(side="right", fill="both", expand=True)

        for F in (pHFrame, DOFrame, ODFrame, TempFrame, StirringFrame, FlowFrame, SettingsFrame):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("pHFrame")

    def show_frame(self, frame_name):
        if frame_name != "SettingsFrame":
            self.current_frame = frame_name
        frame = self.frames[frame_name]
        frame.tkraise()

# --- Blank Frames with only Settings Button ---

class pHFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self._add_settings_button()

    def _add_settings_button(self):
        settings_button = ctk.CTkButton(
            self,
            text="Settings",
            command=lambda: self.controller.show_frame("SettingsFrame"),
            font=("Roboto", 16),
            corner_radius=10,
            fg_color="#E0E0E0",
            text_color="black",
            border_width=2,
            border_color="#4A4A4A"
        )
        settings_button.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

class DOFrame(pHFrame): pass
class ODFrame(pHFrame): pass
class TempFrame(pHFrame): pass
class StirringFrame(pHFrame): pass
class FlowFrame(pHFrame): pass

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        back_button = ctk.CTkButton(
            self,
            text="Back",
            command=lambda: self.controller.show_frame(self.controller.current_frame),
            font=("Roboto", 20),
            corner_radius=10,
            fg_color="#E0E0E0",
            text_color="black",
            border_width=2,
            border_color="#4A4A4A"
        )
        back_button.place(relx=0.5, rely=0.5, anchor="center")

if __name__ == "__main__":
    app = App()
    app.mainloop()
