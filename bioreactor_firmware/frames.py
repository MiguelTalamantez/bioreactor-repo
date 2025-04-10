import customtkinter as ctk

class MainFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        header_text = ctk.CTkLabel(
            self, 
            text="NIMBLE",
            font=("Arial", 36),
            text_color="#007bff"
        )
        header_text.pack(pady=20)
        
        self.run_control_frame = ctk.CTkFrame(self)
        self.run_control_frame.pack(pady=20)
        
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
        
        self.start_button.pack(side="left", padx=10)
        self.time_label.pack(side="left", padx=10)
        
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
        for btn in [self.start_button, self.pause_button, 
                   self.resume_button, self.stop_button]:
            btn.pack_forget()
        
        if not self.parent.is_running:
            self.start_button.pack(side="left", padx=10)
        elif self.parent.is_running and not self.parent.is_paused:
            self.pause_button.pack(side="left", padx=10)
        else:
            self.resume_button.pack(side="left", padx=10)
            self.stop_button.pack(side="left", padx=10)
            
        self.time_label.pack(side="left", padx=10)

class StatsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        header_text = ctk.CTkLabel(
            self, text="Bioreactor Status", font=("Arial", 36), text_color="#007bff"
        )
        header_text.pack(pady=20)

        stats_frame = ctk.CTkFrame(self)
        stats_frame.pack(pady=20, fill="both", expand=True)

        stats_frame.grid_columnconfigure(0, weight=1, uniform="column")
        stats_frame.grid_columnconfigure(1, weight=1, uniform="column")

        ctk.CTkLabel(
            stats_frame, text="Measurement", font=("Arial", 18, "bold")
        ).grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(
            stats_frame, text="Value", font=("Arial", 18, "bold")
        ).grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        measurements = [
            ("Temperature", f"{parent.temperature:.1f}°C"),
            ("pH", f"{parent.ph:.1f}"),
            ("Optical Density", f"{parent.optical_density:.1f}"),
            ("Dissolved Oxygen", f"{parent.dissolved_oxygen:.1f} mg/L")
        ]
        
        for idx, (measurement, value) in enumerate(measurements, 1):
            ctk.CTkLabel(stats_frame, text=measurement, font=("Arial", 14)).grid(row=idx, column=0, padx=10, pady=5, sticky="ew")
            ctk.CTkLabel(stats_frame, text=value, font=("Arial", 14)).grid(row=idx, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkButton(
            self,
            text="Back",
            command=lambda: parent.show_frame(MainFrame)
        ).pack(pady=20)

class SetpointsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.run_duration_value = 24 * 60
        self.temperature_value = 25.0
        self.ph_value = 7.0
        self.labels = {}

        header_text = ctk.CTkLabel(
            self,
            text="Control Parameters",
            font=("Arial", 36),
            text_color="#007bff"
        )
        header_text.pack(pady=20)
        
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(pady=20, fill="both", expand=True)
        
        for col in range(4):
            control_frame.grid_columnconfigure(col, weight=1, uniform="column")
        
        self._create_duration_row(control_frame, 0)
        self._create_parameter_row(control_frame, "Temperature", 1, "°C", self.update_temp)
        self._create_parameter_row(control_frame, "pH", 2, "", self.update_ph)
        
        ctk.CTkButton(
            self,
            text="Back",
            command=lambda: self.master.show_frame(MainFrame)
        ).pack(pady=20)

    def _create_duration_row(self, frame, row):
        label = "Run Duration"
        ctk.CTkLabel(frame, text=label, font=("Arial", 14)).grid(row=row, column=0, padx=10, pady=10, sticky="w")
        
        hours = self.run_duration_value // 60
        minutes = self.run_duration_value % 60
        value_label = ctk.CTkLabel(
            frame, 
            text=f"{hours}h {minutes}m",
            font=("Arial", 14)
        )
        value_label.grid(row=row, column=1, padx=10, pady=10)
        self.labels[label] = value_label
        
        button_frame = ctk.CTkFrame(frame)
        button_frame.grid(row=row, column=2, columnspan=2, sticky="ew")
        
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
        
        header_text = ctk.CTkLabel(self, text="Settings", font=("Arial", 36), text_color="#007bff")
        header_text.pack(pady=20)
        
        settings_frame = ctk.CTkFrame(self)
        settings_frame.pack(pady=20)
        
        ctk.CTkLabel(settings_frame, text="edit the code lol").pack()
        
        ctk.CTkButton(
            self,
            text="Back",
            command=lambda: parent.show_frame(MainFrame)
        ).pack(pady=20)