import customtkinter as ctk
import tkinter as tk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Application Configuration
        self.title("Bioreactor UI")
        self.geometry("800x480")  # Dimensions for a 5-inch screen
        self.resizable(False, False)

        # Set a lighter background color
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Create Frames and Navigation
        self.frames = {}
        self.current_frame = None  # Track the current frame for back navigation
        self._create_navigation()
        self._create_frames()

    def _create_navigation(self):
        """Create the vertical navigation bar on the left."""
        nav_frame = ctk.CTkFrame(self, width=150)
        nav_frame.pack(side="left", fill="y")

        # Navigation Buttons (no gaps, with enhanced styling)
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
                height=80,
                font=("Roboto", 20),
                border_width=2,
                corner_radius=10,
                fg_color="#E0E0E0",
                text_color="black",
                border_color="#4A4A4A"
            ).pack(fill="x")

    def _create_frames(self):
        """Create all sensor frames."""
        container = ctk.CTkFrame(self)
        container.pack(side="right", fill="both", expand=True)

        for F in (pHFrame, DOFrame, ODFrame, TempFrame, StirringFrame, FlowFrame, SettingsFrame):
            frame = F(container, self)  # Pass both parent and controller
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("pHFrame")

    def show_frame(self, frame_name):
        """Raise the specified frame to the top."""
        if frame_name != "SettingsFrame":
            self.current_frame = frame_name
        frame = self.frames[frame_name]
        frame.tkraise()


class pHFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller  # Store controller for later use

        # Center text in the middle of the frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text="pH Sensor Data\nCurrent pH: 7.0",
            font=("Roboto", 30),
            anchor="center"
        ).grid(row=0, column=0)

        # Settings Button
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


class DOFrame(pHFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)  # Pass both arguments
        # Clear existing widgets from parent class
        for widget in self.winfo_children():
            widget.destroy()

        # Add new content
        ctk.CTkLabel(
            self,
            text="Dissolved Oxygen Sensor Data\nCurrent DO: 5.2 mg/L",
            font=("Roboto", 30),
            anchor="center"
        ).grid(row=0, column=0)

        # Re-add Settings Button
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


class ODFrame(pHFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        for widget in self.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self,
            text="Optical Density Sensor Data\nCurrent OD: 0.85",
            font=("Roboto", 30),
            anchor="center"
        ).grid(row=0, column=0)

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


class TempFrame(pHFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        for widget in self.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self,
            text="Temperature Sensor Data\nCurrent Temperature: 37°C",
            font=("Roboto", 30),
            anchor="center"
        ).grid(row=0, column=0)

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


class StirringFrame(pHFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        for widget in self.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self,
            text="Stirring Control\nCurrent Speed: 200 RPM",
            font=("Roboto", 30),
            anchor="center"
        ).grid(row=0, column=0)

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


class FlowFrame(pHFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        for widget in self.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self,
            text="Flow Control\nCurrent Rate: 5 L/min",
            font=("Roboto", 30),
            anchor="center"
        ).grid(row=0, column=0)

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


class SettingsFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Back Button
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
