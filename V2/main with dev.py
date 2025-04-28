import customtkinter as ctk
import tkinter as tk
from datetime import timedelta
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import RPi.GPIO as GPIO
import threading
import time

# Hardware Constants
STEP_PIN = 19
DIR_PIN = 21

# UI Constants
HEADER_COLOR = "#B0C4DE"
LABEL_COLOR = "#E0E0E0"
NAV_TEXT_COLOR = "#D6EAF8"
CURRENT_OK_COLOR = "#6FCF97"
CURRENT_WARN_COLOR = "#FFA94D"
SET_COLOR = "#5DADE2"
BG_DARK = "#1a1a1a"
BG_MED = "#2b2b2b"
BTN_BG = "#404040"
DEV_COLOR = "#8E44AD"

class KPMP10PumpController:
    def __init__(self, step_pin=STEP_PIN, dir_pin=DIR_PIN):
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.running = False
        self.thread = None
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)

    def run(self, direction=1, steps=200, speed=0.001):
        if self.running:
            return
        self.running = True
        GPIO.output(self.dir_pin, direction)
        
        def worker():
            for _ in range(steps):
                if not self.running:
                    break
                GPIO.output(self.step_pin, 1)
                time.sleep(speed)
                GPIO.output(self.step_pin, 0)
                time.sleep(speed)
            self.running = False
            
        self.thread = threading.Thread(target=worker, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)

    def cleanup(self):
        self.stop()
        GPIO.cleanup()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
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
        self.auto_shutoff_time = 60
        self.process_name = "Default Process"
        self.process_active = False
        self.remaining_time = 0
        self.timer_id = None
        self.device_states = {
            "pumps": {f"Pump {i}": "STOP" for i in range(1,5)},
            "led": "OFF",
            "motor": "STOP"
        }

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
            ("Setup", "SetupFrame")
        ]

        for text, frame_name in buttons:
            ctk.CTkButton(
                button_container,
                text=text,
                command=lambda name=frame_name: self.show_frame(name),
                height=60,
                font=("Roboto Mono", 15),
                border_width=1,
                corner_radius=8,
                fg_color=BTN_BG,
                text_color=NAV_TEXT_COLOR,
                border_color="#4A4A4A",
                width=140
            ).pack(fill="x", pady=2, padx=2)

    def _create_frames(self):
        container = ctk.CTkFrame(self, fg_color=BG_DARK)
        container.pack(side="right", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for F in (pHFrame, DOFrame, ODFrame, TempFrame, StirringFrame, FlowFrame, SetupFrame, DeveloperFrame):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("pHFrame")

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()
        if hasattr(frame, "update_process_controls"):
            frame.update_process_controls()
        self.current_frame = frame_name

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
        self._create_condensed_status_table()

    def _create_process_control(self):
        control_frame = ctk.CTkFrame(self, fg_color=BG_MED, corner_radius=8)
        control_frame.pack(pady=4, padx=4, fill="x")

        self.process_text = ctk.CTkLabel(
            control_frame,
            text=f"Process Active: {self.controller.process_name}",
            font=("Roboto Mono", 14),
            text_color=LABEL_COLOR
        )
        self.process_text.pack(side="left", padx=10)

        self.timer_label = ctk.CTkLabel(
            control_frame,
            text="00:00:00",
            font=("Roboto Mono", 14, "bold"),
            text_color=HEADER_COLOR
        )
        self.timer_label.pack(side="left", padx=10)

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
        if self.controller.process_active and self.controller.auto_shutoff_enabled:
            self.after(1000, self.update_process_controls)

    def _create_condensed_status_table(self):
        if not hasattr(self, "status_data"):
            self.status_data = {"Parameter": {"current": 0.0, "set": 0.0, "units": ""}}
        self.status_table_frame = ctk.CTkFrame(self, fg_color=BG_MED, corner_radius=8)
        self.status_table_frame.pack(pady=(2, 2), padx=4, fill="x")
        self.status_table_frame.grid_columnconfigure(0, weight=1, uniform="col")
        self.status_table_frame.grid_columnconfigure(1, weight=1, uniform="col")
        self.status_table_frame.grid_columnconfigure(2, weight=1, uniform="col")
        self.status_table_frame.grid_columnconfigure(3, weight=1, uniform="col")
        headers = ["Parameter", "Current", "Set", "Units"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(self.status_table_frame, text=header,
                       font=("Roboto Mono", 14, "bold"),
                       text_color=HEADER_COLOR).grid(row=0, column=col, pady=(0, 1), sticky="ew")
        self.status_labels = {}
        for row, (param, values) in enumerate(self.status_data.items(), start=1):
            ctk.CTkLabel(self.status_table_frame, text=param,
                       font=("Roboto Mono", 13),
                       text_color=LABEL_COLOR).grid(row=row, column=0, sticky="w", padx=6)
            current_color = CURRENT_OK_COLOR if values["current"] == values["set"] else CURRENT_WARN_COLOR
            self.status_labels[param] = {
                "current": ctk.CTkLabel(self.status_table_frame, text=f"{values['current']:.2f}",
                                      font=("Roboto Mono", 13),
                                      text_color=current_color),
                "set": ctk.CTkLabel(self.status_table_frame, text=f"{values['set']:.2f}",
                                  font=("Roboto Mono", 13),
                                  text_color=SET_COLOR),
                "units": ctk.CTkLabel(self.status_table_frame, text=values.get("units", ""),
                                  font=("Roboto Mono", 13),
                                  text_color=LABEL_COLOR)
            }
            self.status_labels[param]["current"].grid(row=row, column=1, sticky="ew")
            self.status_labels[param]["set"].grid(row=row, column=2, sticky="ew")
            self.status_labels[param]["units"].grid(row=row, column=3, sticky="ew")

class pHFrame(ParameterFrame):
    def __init__(self, parent, controller):
        self.status_data = {
            "pH": {"current": 6.8, "set": 7.0, "units": ""},
            "Buffer": {"current": 250, "set": 300, "units": "mM"}
        }
        super().__init__(parent, controller)
        self._add_ph_graph()
        self._add_improved_setpoint_controls()

    def _add_ph_graph(self):
        self.graph_frame = ctk.CTkFrame(self, fg_color=BG_MED, corner_radius=8)
        self.graph_frame.pack(pady=(2, 2), padx=4, fill="both", expand=True)
        self.fig = Figure(figsize=(6, 2.5), dpi=100, facecolor=BG_MED)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(BG_DARK)
        self.ax.tick_params(colors='white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white') 
        self.ax.spines['right'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.time_points = []
        self.set_ph = []
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def _add_improved_setpoint_controls(self):
        control_frame = ctk.CTkFrame(self, fg_color=BG_MED, corner_radius=8)
        control_frame.pack(pady=(2, 8), padx=4, fill="x")
        control_frame.grid_columnconfigure(0, weight=1)
        control_frame.grid_columnconfigure(1, weight=1)
        control_frame.grid_columnconfigure(2, weight=1)
        ctk.CTkLabel(control_frame, text="Time (min):", 
                   font=("Roboto Mono", 13)).grid(row=0, column=0, padx=2, sticky="e")
        self.time_entry = ctk.CTkEntry(control_frame, width=70, font=("Roboto Mono", 13))
        self.time_entry.grid(row=0, column=1, padx=2, sticky="w")
        ctk.CTkLabel(control_frame, text="Set pH:", 
                   font=("Roboto Mono", 13)).grid(row=0, column=2, padx=2, sticky="e")
        self.ph_entry = ctk.CTkEntry(control_frame, width=70, font=("Roboto Mono", 13))
        self.ph_entry.grid(row=0, column=3, padx=2, sticky="w")
        btn_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        btn_frame.grid(row=0, column=4, columnspan=2, padx=5)
        ctk.CTkButton(btn_frame, text="Add Setpoint",
                      command=self._add_setpoint,
                      fg_color=BTN_BG,
                      text_color=NAV_TEXT_COLOR,
                      font=("Roboto Mono", 13),
                      width=100).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="Remove Last",
                      command=self._remove_setpoint,
                      fg_color=BTN_BG,
                      text_color=NAV_TEXT_COLOR,
                      font=("Roboto Mono", 13),
                      width=100).pack(side="left", padx=2)

    def _add_setpoint(self):
        try:
            time = float(self.time_entry.get())
            ph = float(self.ph_entry.get())
            self.set_ph.append(ph)
            self.time_points.append(time)
            self._update_plot()
            self.time_entry.delete(0, 'end')
            self.ph_entry.delete(0, 'end')
        except ValueError:
            print("Invalid input values")

    def _remove_setpoint(self):
        if len(self.set_ph) > 0:
            self.set_ph.pop()
            self.time_points.pop()
            self._update_plot()

    def _update_plot(self):
        self.ax.clear()
        self.ax.step(self.time_points, self.set_ph, where='post', 
                   label='Set pH', color=SET_COLOR, linestyle='--')
        self.ax.set_xlabel('Time (min)', color='white')
        self.ax.set_ylabel('pH', color='white')
        self.ax.legend(facecolor=BG_MED, labelcolor='white')
        self.ax.grid(color='#4a4a4a', linestyle='--')
        self.canvas.draw()

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
        self._add_dev_button()

    def _add_dev_button(self):
        dev_button = ctk.CTkButton(
            self,
            text="Developer Mode",
            command=lambda: self.controller.show_frame("DeveloperFrame"),
            font=("Roboto Mono", 14),
            corner_radius=8,
            fg_color=DEV_COLOR,
            text_color="white"
        )
        dev_button.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

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

class DeveloperFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_DARK)
        self.controller = controller
        self.kpmp10 = KPMP10PumpController()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._create_pump_controls()
        self._create_led_controls()
        self._create_motor_controls()
        self._create_back_button()

    def _create_pump_controls(self):
        pump_frame = ctk.CTkFrame(self, fg_color=BG_MED, corner_radius=8)
        pump_frame.pack(pady=10, padx=10, fill="x")
        ctk.CTkLabel(pump_frame, text="Pump Controls",
                   font=("Roboto Mono", 16, "bold"),
                   text_color=HEADER_COLOR).pack(pady=5)
        
        for pump in self.controller.pump_assignments:
            pump_row = ctk.CTkFrame(pump_frame, fg_color="transparent")
            pump_row.pack(fill="x", pady=2, padx=10)
            ctk.CTkLabel(pump_row, text=f"{pump}:",
                       font=("Roboto Mono", 14),
                       text_color=LABEL_COLOR).pack(side="left")
            
            btn_frame = ctk.CTkFrame(pump_row, fg_color="transparent")
            btn_frame.pack(side="right")
            
            ctk.CTkButton(btn_frame, text="▶",
                        command=lambda p=pump: self._pump_action(p, "RIGHT"),
                        width=40,
                        fg_color=DEV_COLOR).pack(side="left", padx=2)
            
            ctk.CTkButton(btn_frame, text="◀",
                        command=lambda p=pump: self._pump_action(p, "LEFT"),
                        width=40,
                        fg_color=DEV_COLOR).pack(side="left", padx=2)
            
            ctk.CTkButton(btn_frame, text="⏹",
                        command=lambda p=pump: self._pump_action(p, "STOP"),
                        width=40,
                        fg_color=CURRENT_WARN_COLOR).pack(side="left", padx=2)

    def _pump_action(self, pump, action):
        if pump == "Pump 1":
            if action == "RIGHT":
                self.kpmp10.run(direction=1)
            elif action == "LEFT":
                self.kpmp10.run(direction=0)
            elif action == "STOP":
                self.kpmp10.stop()
        
        self.controller.device_states["pumps"][pump] = action
        print(f"{pump} {action}")

    def _create_led_controls(self):
        led_frame = ctk.CTkFrame(self, fg_color=BG_MED, corner_radius=8)
        led_frame.pack(pady=10, padx=10, fill="x")
        ctk.CTkLabel(led_frame, text="LED Control",
                   font=("Roboto Mono", 16, "bold"),
                   text_color=HEADER_COLOR).pack(pady=5)
        btn_frame = ctk.CTkFrame(led_frame, fg_color="transparent")
        btn_frame.pack()
        self.led_button = ctk.CTkButton(btn_frame, text="LED: OFF",
                                      command=self._toggle_led,
                                      fg_color=DEV_COLOR)
        self.led_button.pack(pady=5)

    def _toggle_led(self):
        current_state = self.controller.device_states["led"]
        new_state = "OFF" if current_state == "ON" else "ON"
        self.controller.device_states["led"] = new_state
        self.led_button.configure(text=f"LED: {new_state}")
        print(f"LED {new_state}")

    def _create_motor_controls(self):
        motor_frame = ctk.CTkFrame(self, fg_color=BG_MED, corner_radius=8)
        motor_frame.pack(pady=10, padx=10, fill="x")
        ctk.CTkLabel(motor_frame, text="Motor Control",
                   font=("Roboto Mono", 16, "bold"),
                   text_color=HEADER_COLOR).pack(pady=5)
        btn_frame = ctk.CTkFrame(motor_frame, fg_color="transparent")
        btn_frame.pack()
        ctk.CTkButton(btn_frame, text="◀ LEFT",
                    command=lambda: self._motor_action("LEFT"),
                    fg_color=DEV_COLOR).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="⏹ STOP",
                    command=lambda: self._motor_action("STOP"),
                    fg_color=CURRENT_WARN_COLOR).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="RIGHT ▶",
                    command=lambda: self._motor_action("RIGHT"),
                    fg_color=DEV_COLOR).pack(side="left", padx=2)

    def _motor_action(self, action):
        self.controller.device_states["motor"] = action
        print(f"Motor {action}")

    def _create_back_button(self):
        back_button = ctk.CTkButton(
            self,
            text="Back to Setup",
            command=lambda: self.controller.show_frame("SetupFrame"),
            font=("Roboto Mono", 14),
            corner_radius=8,
            fg_color=BTN_BG,
            text_color=HEADER_COLOR
        )
        back_button.place(relx=0.5, rely=1.0, x=0, y=-10, anchor="s")

if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    finally:
        if hasattr(app.frames.get("DeveloperFrame", None), "kpmp10"):
            app.frames["DeveloperFrame"].kpmp10.cleanup()
