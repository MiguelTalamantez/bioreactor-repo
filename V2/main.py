import customtkinter as ctk
import tkinter as tk
from datetime import timedelta

# --- Color Palette ---
HEADER_COLOR = "#B0C4DE"
LABEL_COLOR = "#E0E0E0"
NAV_TEXT_COLOR = "#D6EAF8"
CURRENT_OK_COLOR = "#6FCF97"
CURRENT_WARN_COLOR = "#FFA94D"
SET_COLOR = "#5DADE2"
BG_DARK = "#1a1a1a"
BG_MED = "#2b2b2b"
BTN_BG = "#404040"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Application Configuration
        self.title("Bioreactor Control v2.1")
        self.geometry("800x480")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.frames = {}
        self.current_frame = None
        self.pump_assignments = {
            "Pump 1": "HCl",
            "Pump 2": "NaOH",
            "Pump 3": "Media",
            "Pump 4": "Waste"
        }
        self.auto_shutoff_enabled = False
        self.auto_shutoff_time = 60  # default 60 minutes
        self.process_name = "Default Process"
        self.process_active = False
        self.remaining_time = 0
        self.timer_id = None

        self._create_navigation()
        self._create_frames()

    def _create_navigation(self):
        nav_frame = ctk.CTkFrame(self, width=150, fg_color=BG_MED)
        nav_frame.pack(side="left", fill="y", ipadx=5)

        button_container = ctk.CTkFrame(nav_frame, fg_color="transparent")
        button_container.pack(expand=True)

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
                button_container,
                text=text,
                command=lambda name=frame_name: self.show_frame(name),
                height=70,
                font=("Roboto Mono", 14),
                border_width=1,
                corner_radius=8,
                fg_color=BTN_BG,
                text_color=NAV_TEXT_COLOR,
                border_color="#4A4A4A"
            ).pack(fill="x", pady=2, padx=2)

    def _create_frames(self):
        container = ctk.CTkFrame(self, fg_color=BG_DARK)
        container.pack(side="right", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for F in (pHFrame, DOFrame, ODFrame, TempFrame, StirringFrame, FlowFrame, SetupFrame):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("pHFrame")

    def show_frame(self, frame_name):
        if frame_name != "SetupFrame":
            self.current_frame = frame_name
        frame = self.frames[frame_name]
        frame.tkraise()
        if hasattr(frame, "update_process_controls"):
            frame.update_process_controls()

    def start_process(self):
        if not self.process_active:
            self.process_active = True
            if self.auto_shutoff_enabled:
                self.remaining_time = self.auto_shutoff_time * 60
                self._tick_timer()
            self._update_all_process_controls()
            print(f"Process '{self.process_name}' started")

    def stop_process(self):
        if self.process_active:
            self.process_active = False
            if self.timer_id:
                self.after_cancel(self.timer_id)
                self.timer_id = None
            self._update_all_process_controls()
            print(f"Process '{self.process_name}' stopped")

    def _tick_timer(self):
        if self.process_active and self.auto_shutoff_enabled and self.remaining_time > 0:
            self.remaining_time -= 1
            self._update_all_process_controls()
            self.timer_id = self.after(1000, self._tick_timer)
        else:
            if self.process_active:
                self.stop_process()

    def _update_all_process_controls(self):
        for frame in self.frames.values():
            if hasattr(frame, "update_process_controls"):
                frame.update_process_controls()

class ParameterFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_DARK)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._create_process_control()
        self._create_status_table()
        self._add_setup_button()

    def _create_process_control(self):
        control_frame = ctk.CTkFrame(self, fg_color=BG_MED, corner_radius=8)
        control_frame.pack(pady=4, padx=4, fill="x")

        # Process Name and Status
        self.process_text = ctk.CTkLabel(
            control_frame,
            text=f"Process Active: {self.controller.process_name}",
            font=("Roboto Mono", 14),
            text_color=LABEL_COLOR
        )
        self.process_text.pack(side="left", padx=10)

        # Timer Display
        self.timer_label = ctk.CTkLabel(
            control_frame,
            text="00:00:00",
            font=("Roboto Mono", 14, "bold"),
            text_color=HEADER_COLOR
        )
        self.timer_label.pack(side="left", padx=10)

        # Start/Stop Button (Larger size)
        self.process_button = ctk.CTkButton(
            control_frame,
            text="Start Process" if not self.controller.process_active else "Stop Process",
            command=self._toggle_process,
            font=("Roboto Mono", 16, "bold"),
            fg_color=CURRENT_OK_COLOR if not self.controller.process_active else CURRENT_WARN_COLOR,
            text_color=BG_DARK,
            width=180,
            height=60,
            corner_radius=12
        )
        self.process_button.pack(side="right", padx=10, pady=2)

        self.update_process_controls()

    def _toggle_process(self):
        if self.controller.process_active:
            self.controller.stop_process()
        else:
            self.controller.start_process()
        self.update_process_controls()

    def update_process_controls(self):
        self.process_button.configure(
            text="Stop Process" if self.controller.process_active else "Start Process",
            fg_color=CURRENT_WARN_COLOR if self.controller.process_active else CURRENT_OK_COLOR
        )
        # Timer logic
        if self.controller.process_active and self.controller.auto_shutoff_enabled:
            t = max(0, self.controller.remaining_time)
            time_str = str(timedelta(seconds=t))
            if len(time_str) > 7:
                time_str = time_str[-8:]
            self.timer_label.configure(text=time_str)
        elif self.controller.process_active and not self.controller.auto_shutoff_enabled:
            self.timer_label.configure(text="Manual")
        else:
            self.timer_label.configure(text="00:00:00")
        self.process_text.configure(text=f"Process Active: {self.controller.process_name}")
        # If process is running and auto-shutoff is on, keep updating
        if self.controller.process_active and self.controller.auto_shutoff_enabled:
            self.after(1000, self.update_process_controls)

    def _create_status_table(self):
        if not hasattr(self, "status_data"):
            self.status_data = {"Parameter": {"current": 0.0, "set": 0.0, "units": ""}}
        table_frame = ctk.CTkFrame(self, fg_color=BG_MED, corner_radius=8)
        table_frame.pack(pady=4, padx=4, fill="both", expand=True)
        ctk.CTkLabel(table_frame, text="Parameter Status",
                   font=("Roboto Mono", 16, "bold"),
                   text_color=HEADER_COLOR).grid(row=0, column=0, columnspan=4, pady=(2, 4))
        headers = ["Parameter", "Current", "Set Value", "Units"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(table_frame, text=header,
                       font=("Roboto Mono", 14, "bold"),
                       text_color=HEADER_COLOR).grid(row=1, column=col, padx=6, pady=(2, 2))
        self.status_labels = {}
        for row, (param, values) in enumerate(self.status_data.items(), start=2):
            ctk.CTkLabel(table_frame, text=param,
                       font=("Roboto Mono", 14),
                       text_color=LABEL_COLOR).grid(row=row, column=0, sticky="w", padx=6, pady=(1, 1))
            current_color = CURRENT_OK_COLOR if values["current"] == values["set"] else CURRENT_WARN_COLOR
            self.status_labels[param] = {
                "current": ctk.CTkLabel(table_frame, text=f"{values['current']:.2f}",
                                      font=("Roboto Mono", 14),
                                      text_color=current_color),
                "set": ctk.CTkLabel(table_frame, text=f"{values['set']:.2f}",
                                  font=("Roboto Mono", 14),
                                  text_color=SET_COLOR),
                "units": ctk.CTkLabel(table_frame, text=values.get("units", ""),
                                  font=("Roboto Mono", 14),
                                  text_color=LABEL_COLOR)
            }
            self.status_labels[param]["current"].grid(row=row, column=1, padx=6, pady=(1, 1))
            self.status_labels[param]["set"].grid(row=row, column=2, padx=6, pady=(1, 1))
            self.status_labels[param]["units"].grid(row=row, column=3, padx=6, pady=(1, 1))

    def _add_setup_button(self):
        setup_button = ctk.CTkButton(
            self,
            text="Setup",
            command=lambda: self.controller.show_frame("SetupFrame"),
            font=("Roboto Mono", 14),
            corner_radius=8,
            fg_color=BTN_BG,
            text_color=HEADER_COLOR,
            border_width=1,
            border_color="#4A4A4A",
            width=100,
            height=40
        )
        setup_button.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

class pHFrame(ParameterFrame):
    def __init__(self, parent, controller):
        self.status_data = {
            "pH": {"current": 6.8, "set": 7.0, "units": ""},
            "Buffer": {"current": 250, "set": 300, "units": "mM"}
        }
        super().__init__(parent, controller)

class DOFrame(ParameterFrame):
    def __init__(self, parent, controller):
        self.status_data = {
            "Dissolved O₂": {"current": 98.4, "set": 95.0, "units": "%"},
            "O₂ Flow": {"current": 2.5, "set": 2.8, "units": "L/min"}
        }
        super().__init__(parent, controller)

class ODFrame(ParameterFrame):
    def __init__(self, parent, controller):
        self.status_data = {
            "Optical Density": {"current": 0.42, "set": 0.50, "units": "AU"}
        }
        super().__init__(parent, controller)

class TempFrame(ParameterFrame):
    def __init__(self, parent, controller):
        self.status_data = {
            "Temperature": {"current": 37.2, "set": 37.0, "units": "°C"}
        }
        super().__init__(parent, controller)

class StirringFrame(ParameterFrame):
    def __init__(self, parent, controller):
        self.status_data = {
            "Stir Speed": {"current": 300, "set": 350, "units": "RPM"}
        }
        super().__init__(parent, controller)

class FlowFrame(ParameterFrame):
    def __init__(self, parent, controller):
        self.status_data = {
            "Flow Rate": {"current": 2.0, "set": 2.5, "units": "mL/min"}
        }
        super().__init__(parent, controller)

class SetupFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_DARK)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._create_process_settings()
        self._create_pump_assignment_ui()

    def _create_process_settings(self):
        settings_frame = ctk.CTkFrame(self, fg_color=BG_MED, corner_radius=8)
        settings_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(
            settings_frame,
            text="Process Name:",
            font=("Roboto Mono", 14),
            text_color=LABEL_COLOR
        ).pack(side="left", padx=10)
        
        self.process_entry = ctk.CTkEntry(
            settings_frame,
            font=("Roboto Mono", 14),
            width=200
        )
        self.process_entry.pack(side="left", padx=5)
        self.process_entry.insert(0, self.controller.process_name)
        self.process_entry.bind("<FocusOut>", self._update_process_name)
        self.process_entry.bind("<Return>", self._update_process_name)

    def _update_process_name(self, event=None):
        new_name = self.process_entry.get()
        if new_name != self.controller.process_name:
            self.controller.process_name = new_name
            print(f"Process name updated to: {self.controller.process_name}")
            self.controller._update_all_process_controls()

    def _create_pump_assignment_ui(self):
        main_frame = ctk.CTkFrame(self, fg_color=BG_MED, corner_radius=8)
        main_frame.pack(pady=10, padx=10, fill="both", expand=True)

        ctk.CTkLabel(main_frame, text="Pump Configuration",
                   font=("Roboto Mono", 16, "bold"),
                   text_color=HEADER_COLOR).pack(pady=5)

        chemicals = ["HCl", "NaOH", "Media", "Buffer", "Waste"]
        for pump in self.controller.pump_assignments:
            row_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=2, padx=10)
            ctk.CTkLabel(row_frame, text=f"{pump}:",
                       font=("Roboto Mono", 14),
                       text_color=LABEL_COLOR,
                       width=80).pack(side="left")
            option_menu = ctk.CTkOptionMenu(
                row_frame,
                values=chemicals,
                command=lambda value, p=pump: self._update_pump_assignment(p, value),
                fg_color=BTN_BG,
                button_color="#4A4A4A",
                text_color=HEADER_COLOR,
                dropdown_fg_color=BG_MED,
                dropdown_text_color=HEADER_COLOR,
                font=("Roboto Mono", 14)
            )
            option_menu.set(self.controller.pump_assignments[pump])
            option_menu.pack(side="right", fill="x", expand=True)

        # --- Auto-Shutoff Controls ---
        shutoff_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        shutoff_frame.pack(fill="x", pady=10, padx=10)
        self.shutoff_switch = ctk.CTkSwitch(
            shutoff_frame,
            text="Enable Auto-Shutoff",
            font=("Roboto Mono", 14),
            text_color=LABEL_COLOR,
            command=self._toggle_shutoff
        )
        self.shutoff_switch.pack(side="left", padx=5)
        self.shutoff_switch.select() if self.controller.auto_shutoff_enabled else self.shutoff_switch.deselect()
        ctk.CTkLabel(
            shutoff_frame,
            text="Time (min):",
            font=("Roboto Mono", 14),
            text_color=LABEL_COLOR,
            width=90
        ).pack(side="left", padx=8)
        self.shutoff_time_entry = ctk.CTkEntry(
            shutoff_frame,
            width=60,
            font=("Roboto Mono", 14)
        )
        self.shutoff_time_entry.pack(side="left", padx=2)
        self.shutoff_time_entry.insert(0, str(self.controller.auto_shutoff_time))
        self.shutoff_time_entry.bind("<FocusOut>", self._update_shutoff_time)
        self.shutoff_time_entry.bind("<Return>", self._update_shutoff_time)
        back_button = ctk.CTkButton(
            self,
            text="Back to Dashboard",
            command=lambda: self.controller.show_frame(self.controller.current_frame),
            font=("Roboto Mono", 14),
            corner_radius=8,
            fg_color=BTN_BG,
            text_color=HEADER_COLOR,
            border_width=1,
            border_color="#4A4A4A"
        )
        back_button.place(relx=0.5, rely=1.0, x=0, y=-10, anchor="s")

    def _update_pump_assignment(self, pump, chemical):
        self.controller.pump_assignments[pump] = chemical
        print(f"Updated {pump} to {chemical}")

    def _toggle_shutoff(self):
        self.controller.auto_shutoff_enabled = bool(self.shutoff_switch.get())
        print(f"Auto-shutoff enabled: {self.controller.auto_shutoff_enabled}")
        self.controller._update_all_process_controls()

    def _update_shutoff_time(self, event=None):
        try:
            time = int(self.shutoff_time_entry.get())
            if time > 0:
                self.controller.auto_shutoff_time = time
                print(f"Auto-shutoff time set to: {time} min")
            else:
                raise ValueError
        except ValueError:
            self.shutoff_time_entry.delete(0, "end")
            self.shutoff_time_entry.insert(0, str(self.controller.auto_shutoff_time))

if __name__ == "__main__":
    app = App()
    app.mainloop()
