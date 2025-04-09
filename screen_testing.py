import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NIMBLE")
        window_width=600
        window_height=400
        screen_width=self.winfo_screenwidth()
        screen_height=self.winfo_screenheight()
        center_x=int((screen_width/2)-(window_width/2))
        center_y=int((screen_height/2)-(window_height/2))
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.resizable(False,False)
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.frames={}
        for F in (MainFrame,StatsFrame,SetpointsFrame,SettingsFrame):
            frame=F(self)
            self.frames[F]=frame
            frame.grid(row=0,column=0,sticky="nsew")
        self.show_frame(MainFrame)
    
    def show_frame(self,cont):
        frame=self.frames[cont]
        frame.tkraise()

class MainFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Header Section
        header_text = ctk.CTkLabel(
            self, text="NIMBLE", font=("Arial", 36), text_color="#007bff"
        )
        header_text.pack(pady=20)  # Add padding to position the header

        # Options Frame
        options_frame = ctk.CTkFrame(self)
        options_frame.pack(pady=20)  # Add padding to position the frame

        # Buttons for Navigation
        ctk.CTkButton(
            options_frame,
            text="View Bioreactor Stats",
            command=lambda: parent.show_frame(StatsFrame)  # Navigate to StatsFrame
        ).pack(side="left", padx=10)  # Align button to the left with padding

        ctk.CTkButton(
            options_frame,
            text="Set Control System Setpoints",
            command=lambda: parent.show_frame(SetpointsFrame)  # Navigate to SetpointsFrame
        ).pack(side="left", padx=10)  # Align button to the left with padding

        ctk.CTkButton(
            options_frame,
            text="Settings",
            command=lambda: parent.show_frame(SettingsFrame)  # Navigate to SettingsFrame
        ).pack(side="left", padx=10)  # Align button to the left with padding

class StatsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Header Section
        header_text = ctk.CTkLabel(
            self, text="Bioreactor Status", font=("Arial", 36), text_color="#007bff"
        )
        header_text.pack(pady=20)

        # Main Stats Frame
        stats_frame = ctk.CTkFrame(self)
        stats_frame.pack(pady=20, fill="both", expand=True)

        # Configure grid layout for two columns
        stats_frame.grid_columnconfigure(0, weight=1, uniform="column")  # Column for measurements
        stats_frame.grid_columnconfigure(1, weight=1, uniform="column")  # Column for values

        # Table Header Row
        ctk.CTkLabel(
            stats_frame, text="Measurement", font=("Arial", 18, "bold")
        ).grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        ctk.CTkLabel(
            stats_frame, text="Value", font=("Arial", 18, "bold")
        ).grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Measurement Data
        measurements = ["Temperature", "pH", "Optical Density", "Dissolved Oxygen"]  # List of measurement names
        values = ["25°C", "7.0", "0.5", "5.0 mg/L"]  # Corresponding values for each measurement

        # Populate the table with measurements and their values
        for i in range(len(measurements)):
            # Add measurement label to the first column
            ctk.CTkLabel(
                stats_frame, text=measurements[i], font=("Arial", 14)
            ).grid(row=i + 1, column=0, padx=10, pady=5, sticky="ew")

            # Add corresponding value to the second column
            ctk.CTkLabel(
                stats_frame, text=values[i], font=("Arial", 14)
            ).grid(row=i + 1, column=1, padx=10, pady=5, sticky="ew")

        # Back Button Section
        ctk.CTkButton(
            self,
            text="Back",
            command=lambda: parent.show_frame(MainFrame)  # Navigate back to the main frame
        ).pack(pady=20)

class SetpointsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Initialize default setpoint values
        self.temp_value = 25.0  # Default temperature value in °C
        self.ph_value = 7.0     # Default pH value

        # Header Section
        header_text = ctk.CTkLabel(
            self, text="Input Value", font=("Arial", 36), text_color="#007bff"
        )
        header_text.pack(pady=20)

        # Main Setpoints Frame
        setpoints_frame = ctk.CTkFrame(self)
        setpoints_frame.pack(pady=20, fill="both", expand=True)

        # Configure grid layout for uniform column spacing
        for col in range(4):
            setpoints_frame.grid_columnconfigure(col, weight=1, uniform="column")

        # Add rows for Temperature and pH setpoints
        self.create_row(
            setpoints_frame, "Temperature", 0, self.temp_value, "°C", self.update_temp
        )
        self.create_row(
            setpoints_frame, "pH", 1, self.ph_value, "", self.update_ph
        )

        # Back Button Section
        ctk.CTkButton(
            self,
            text="Back",
            command=lambda: parent.show_frame(MainFrame)
        ).pack(pady=20)

    def create_row(self, frame, label, row, value, unit, callback):
        """
        Creates a row in the setpoints frame with a label, value display,
        and increment/decrement buttons.

        Parameters:
            frame (CTkFrame): The parent frame where the row will be added.
            label (str): The label text (e.g., "Temperature").
            row (int): The row index in the grid layout.
            value (float): The initial value to display.
            unit (str): The unit of measurement (e.g., "°C").
            callback (function): The function to call when buttons are clicked.
        """
        
        # Label for the parameter name
        ctk.CTkLabel(frame, text=label, font=("Arial", 14)).grid(
            row=row, column=0, padx=10, pady=10, sticky="w"
        )

        # Label to display the current value with its unit
        self.value_label = ctk.CTkLabel(
            frame, text=f"{value}{unit}", font=("Arial", 14)
        )
        self.value_label.grid(row=row, column=1, padx=10, pady=10)

        # Decrement button (-)
        ctk.CTkButton(
            frame,
            text="-",
            command=lambda: callback(-0.5 if label == "Temperature" else -0.1),
        ).grid(row=row, column=2, padx=5, pady=10)

        # Increment button (+)
        ctk.CTkButton(
            frame,
            text="+",
            command=lambda: callback(0.5 if label == "Temperature" else 0.1),
        ).grid(row=row, column=3, padx=5, pady=10)

    def update_temp(self, change):
        """
        Updates the temperature value and refreshes its display.
        Parameters:
            change (float): The amount to adjust the temperature by.
                           Positive for increment; negative for decrement.
        """
        
        self.temp_value += change
        self.value_label.configure(text=f"{self.temp_value:.1f}°C")

    def update_ph(self, change):
        """
        Updates the pH value and refreshes its display.
        Parameters:
            change (float): The amount to adjust the pH by.
                           Positive for increment; negative for decrement.
        """
        
        self.ph_value += change
        self.value_label.configure(text=f"{self.ph_value:.1f}")

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Header
        header_text = ctk.CTkLabel(self, text="Settings", font=("Arial", 36), text_color="#007bff")
        header_text.pack(pady=20)
        
        # Settings Frame
        settings_frame = ctk.CTkFrame(self)
        settings_frame.pack(pady=20)
        
        # Font Size Option
        ctk.CTkLabel(settings_frame, text="Font Size:").pack()
        ctk.CTkOptionMenu(settings_frame, values=["Small", "Medium", "Large"]).pack()
        
        # Color Mode Option
        ctk.CTkLabel(settings_frame, text="Color Mode:").pack()
        ctk.CTkOptionMenu(settings_frame, values=["Dark Mode", "Light Mode"]).pack()
        
        # Back Button
        ctk.CTkButton(self, text="Back", command=lambda: parent.show_frame(MainFrame)).pack(pady=20)

if __name__=="__main__":
    app=App()
    app.mainloop()