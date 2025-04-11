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
        self._create_navigation()
        self._create_frames()

    def _create_navigation(self):
        """Create the vertical navigation bar on the left."""
        nav_frame = ctk.CTkFrame(self, width=150)
        nav_frame.pack(side="left", fill="y")

        # Navigation Buttons (no gaps)
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
                height=80,  # Increased height to fill space and make text bigger
                font=("Roboto", 20),  # Bigger font for better readability
            ).pack(fill="x")  # Fill horizontally with no gaps

    def _create_frames(self):
        """Create all sensor frames."""
        container = ctk.CTkFrame(self)
        container.pack(side="right", fill="both", expand=True)

        for F in (pHFrame, DOFrame, ODFrame, TempFrame, StirringFrame, FlowFrame):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("pHFrame")  # Show the first frame by default

    def show_frame(self, frame_name):
        """Raise the specified frame to the top."""
        frame = self.frames[frame_name]
        frame.tkraise()


class pHFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Center text in the middle of the frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text="pH Sensor Data\nCurrent pH: 7.0",
            font=("Roboto", 30),  # Bigger font for better readability
            anchor="center"
        ).grid(row=0, column=0)


class DOFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Center text in the middle of the frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text="Dissolved Oxygen Sensor Data\nCurrent DO: 5.2 mg/L",
            font=("Roboto", 30),  # Bigger font for better readability
            anchor="center"
        ).grid(row=0, column=0)


class ODFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Center text in the middle of the frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text="Optical Density Sensor Data\nCurrent OD: 0.85",
            font=("Roboto", 30),  # Bigger font for better readability
            anchor="center"
        ).grid(row=0, column=0)


class TempFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Center text in the middle of the frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text="Temperature Sensor Data\nCurrent Temperature: 37°C",
            font=("Roboto", 30),  # Bigger font for better readability
            anchor="center"
        ).grid(row=0, column=0)


class StirringFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Center text in the middle of the frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text="Stirring Control\nCurrent Speed: 200 RPM",
            font=("Roboto", 30),  # Bigger font for better readability
            anchor="center"
        ).grid(row=0, column=0)


class FlowFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Center text in the middle of the frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text="Flow Control\nCurrent Rate: 5 L/min",
            font=("Roboto", 30),  # Bigger font for better readability
            anchor="center"
        ).grid(row=0, column=0)


if __name__ == "__main__":
    app = App()
    app.mainloop()
