import customtkinter as ctk
import time

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Application Configuration
        self.title("NIMBLE")
        self._configure_window()
        self._initialize_variables()
        self._create_frames()
        
    def _configure_window(self):
        window_width = 600
        window_height = 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int((screen_width/2) - (window_width/2))
        center_y = int((screen_height/2) - (window_height/2))
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.resizable(False, False)
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
    def _initialize_variables(self):
        # Bioreactor State Variables
        self.is_running = False
        self.is_paused = False
        self.remaining_time = 0  # In seconds
        self.total_duration = 0  # In seconds
        self.run_duration = 24 * 60  # Default duration in minutes (24 hours)
        self.after_id = None
        
        # Process Variables
        self.temperature = 25.0
        self.ph = 7.0
        self.dissolved_oxygen = 5.0
        self.optical_density = 0.5

        # Theme Configuration
        self.appearance_mode = "Dark"
        self.time_remaining_str = ctk.StringVar(value="00:00:00")

    def _create_frames(self):
        self.frames = {}
        for F in (MainFrame, StatsFrame, SetpointsFrame, SettingsFrame):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainFrame)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    def toggle_run(self):
        if not self.is_running:
            self.start_run()
        else:
            self.pause_run()
    
    def start_run(self):
        self.is_running = True
        self.is_paused = False
        self.total_duration = self.run_duration * 60  # Convert minutes to seconds
        self.remaining_time = self.total_duration
        self._update_timer()
        self.frames[MainFrame].update_buttons()
    
    def pause_run(self):
        self.is_paused = True
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None
        self.frames[MainFrame].update_buttons()
    
    def resume_run(self):
        self.is_paused = False
        self._update_timer()
        self.frames[MainFrame].update_buttons()
    
    def stop_run(self):
        self.is_running = False
        self.is_paused = False
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None
        self.time_remaining_str.set("00:00:00")
        self.frames[MainFrame].update_buttons()
    
    def _update_timer(self):
        if self.is_running and not self.is_paused:
            if self.remaining_time > 0:
                self.remaining_time -= 1
                self.time_remaining_str.set(self._format_time(self.remaining_time))
                self.after_id = self.after(1000, self._update_timer)
            else:
                self.stop_run()
    
    def _format_time(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def update_theme(self, new_mode):
        self.appearance_mode = new_mode
        ctk.set_appearance_mode(new_mode)

class MainFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # Header
        header_text = ctk.CTkLabel(
            self, 
            text="NIMBLE",
            font=("Arial", 36),
            text_color="#007bff"
        )
        header_text.pack(pady=20)
        
        # Run Control Section
        self.run_control_frame = ctk.CTkFrame(self)
        self.run_control_frame.pack(pady=20)
        
        # Control Buttons
        self.start_button = ctk.CTkButton(
            self.run_control_frame,
            text="Start Run",
            command=self.parent.toggle_run
        )
        
        self.pause_button = ctk.CTkButton(
            self.run_control_frame,
            text="Pause",
            command=self.parent.pause_run
        )
        
        self.resume_button = ctk.CTkButton(
            self.run_control_frame,
            text="Resume",
            command=self.parent.resume_run
        )
        
        self.stop_button = ctk.CTkButton(
            self.run_control_frame,
            text="Stop",
            command=self.parent.stop_run
        )
        
        self.time_label = ctk.CTkLabel(
            self.run_control_frame,
            textvariable=self.parent.time_remaining_str,
            font=("Arial", 14)
        )
        
        # Initial layout
        self.start_button.pack(side="left", padx=10)
        self.time_label.pack(side="left", padx=10)
        
        # Navigation Buttons
        options_frame = ctk.CTkFrame(self)
        options_frame.pack(pady=20)
        
        buttons = [
            ("View Bioreactor Stats", StatsFrame),
            ("Set Control Parameters", SetpointsFrame),
            ("Settings", SettingsFrame)
        ]
        
        for text, frame_class in buttons:
            ctk.CTkButton(
                options_frame,
                text=text,
                command=lambda fc=frame_class: self.parent.show_frame(fc)
            ).pack(side="left", padx=10)
    
    def update_buttons(self):
        # Clear existing buttons
        for btn in [self.start_button, self.pause_button, 
                   self.resume_button, self.stop_button]:
            btn.pack_forget()
        
        # Show appropriate buttons
        if not self.parent.is_running:
            self.start_button.pack(side="left", padx=10)
        elif self.parent.is_running and not self.parent.is_paused:
            self.pause_button.pack(side="left", padx=10)
        else:  # Paused state
            self.resume_button.pack(side="left", padx=10)
            self.stop_button.pack(side="left", padx=10)
            
        self.time_label.pack(side="left", padx=10)

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
        stats_frame.grid_columnconfigure(0, weight=1, uniform="column")
        stats_frame.grid_columnconfigure(1, weight=1, uniform="column")

        # Table Header Row
        ctk.CTkLabel(
            stats_frame, text="Measurement", font=("Arial", 18, "bold")
        ).grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(
            stats_frame, text="Value", font=("Arial", 18, "bold")
        ).grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Measurement Data
        measurements = [
            ("Temperature", f"{parent.temperature:.1f}°C"),
            ("pH", f"{parent.ph:.1f}"),
            ("Optical Density", f"{parent.optical_density:.1f}"),
            ("Dissolved Oxygen", f"{parent.dissolved_oxygen:.1f} mg/L")
        ]
        
        for idx, (measurement, value) in enumerate(measurements, 1):
            ctk.CTkLabel(stats_frame, text=measurement, font=("Arial", 14)).grid(row=idx, column=0, padx=10, pady=5, sticky="ew")
            ctk.CTkLabel(stats_frame, text=value, font=("Arial", 14)).grid(row=idx, column=1, padx=10, pady=5, sticky="ew")
        
        # Back Button
        ctk.CTkButton(
            self,
            text="Back",
            command=lambda: parent.show_frame(MainFrame)
        ).pack(pady=20)

class SetpointsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Initialize default values
        self.run_duration_value = 24 * 60  # Default duration in minutes (24 hours)
        self.temperature_value = 25.0  # Corrected attribute name
        self.ph_value = 7.0
        self.labels = {}

        # Header Section
        header_text = ctk.CTkLabel(
            self,
            text="Control Parameters",
            font=("Arial", 36),
            text_color="#007bff"
        )
        header_text.pack(pady=20)
        
        # Control Panel
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(pady=20, fill="both", expand=True)
        
        # Configure grid
        for col in range(4):
            control_frame.grid_columnconfigure(col, weight=1, uniform="column")
        
        # Add parameter rows
        self._create_duration_row(control_frame, 0)
        self._create_parameter_row(control_frame, "Temperature", 1, "°C", self.update_temp)
        self._create_parameter_row(control_frame, "pH", 2, "", self.update_ph)
        
        # Back button
        ctk.CTkButton(
            self,
            text="Back",
            command=lambda: self.master.show_frame(MainFrame)
        ).pack(pady=20)
    
    def _create_duration_row(self, frame, row):
        label = "Run Duration"
        ctk.CTkLabel(frame, text=label, font=("Arial", 14)).grid(row=row, column=0, padx=10, pady=10, sticky="w")
        
        # Initial value display
        hours = self.run_duration_value // 60
        minutes = self.run_duration_value % 60
        value_label = ctk.CTkLabel(
            frame, 
            text=f"{hours}h {minutes}m",
            font=("Arial", 14)
        )
        value_label.grid(row=row, column=1, padx=10, pady=10)
        self.labels[label] = value_label
        
        # Button container frame
        button_frame = ctk.CTkFrame(frame)
        button_frame.grid(row=row, column=2, columnspan=2, sticky="ew")
        
        # Duration control buttons
        buttons = [
            ("-1m", -1),
            ("+1m", 1),
            ("-30m", -30),
            ("+30m", 30)
        ]
        
        for text, delta in buttons:
            ctk.CTkButton(
                button_frame,
                text=text,
                width=60,
                command=lambda d=delta: self._adjust_duration(d)
            ).pack(side="left", padx=2)
    
    def _adjust_duration(self, delta):
        new_value = max(0, self.run_duration_value + delta)
        self.run_duration_value = new_value
        hours = new_value // 60
        minutes = new_value % 60
        self.labels["Run Duration"].configure(text=f"{hours}h {minutes}m")
        self.master.run_duration = new_value
    
    def _create_parameter_row(self, frame, label, row, unit, callback):
        ctk.CTkLabel(frame, text=label, font=("Arial", 14)).grid(row=row, column=0, padx=10, pady=10, sticky="w")
        
        value = getattr(self, f"{label.lower()}_value")
        value_label = ctk.CTkLabel(
            frame, 
            text=f"{value}{unit}",
            font=("Arial", 14)
        )
        value_label.grid(row=row, column=1, padx=10, pady=10)
        self.labels[label] = value_label
        
        ctk.CTkButton(
            frame,
            text="-",
            font=("Arial", 18),
            command=lambda: self._adjust_value(label, -0.5 if label == "Temperature" else -0.1, callback)
        ).grid(row=row, column=2, padx=5, pady=10)
        
        ctk.CTkButton(
            frame,
            text="+",
            command=lambda: self._adjust_value(label, 0.5 if label == "Temperature" else 0.1, callback)
        ).grid(row=row, column=3, padx=5, pady=10)
    
    def _adjust_value(self, label, amount, callback):
        attr_name = f"{label.lower()}_value"
        current_value = getattr(self, attr_name)
        new_value = max(0, current_value + amount)
        setattr(self, attr_name, new_value)
        self.labels[label].configure(text=f"{new_value:.1f}{'°C' if label == 'Temperature' else ''}")
        callback(new_value)
    
    def update_temp(self, value):
        self.master.temperature = value
    
    def update_ph(self, value):
        self.master.ph = value

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Header
        header_text = ctk.CTkLabel(self, text="Settings", font=("Arial", 36), text_color="#007bff")
        header_text.pack(pady=20)
        
        # Settings Frame
        settings_frame = ctk.CTkFrame(self)
        settings_frame.pack(pady=20)
        
        # Preserve existing commented code
        ctk.CTkLabel(settings_frame, text="edit the code lol").pack()
        
        # Back Button
        ctk.CTkButton(
            self,
            text="Back",
            command=lambda: parent.show_frame(MainFrame)
        ).pack(pady=20)

if __name__ == "__main__":
    app = App()
    app.mainloop()
