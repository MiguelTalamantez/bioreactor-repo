import customtkinter as ctk
import tkinter as tk

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
        self._create_navigation()
        self._create_frames()

    def _create_navigation(self):
        nav_frame = ctk.CTkFrame(self, width=150, fg_color=BG_MED)
        nav_frame.pack(side="left", fill="y", ipadx=5)

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

class ParameterFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_DARK)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._create_status_table()
        self._add_setup_button()

    def _create_status_table(self):
        if not hasattr(self, "status_data"):
            self.status_data = {"Parameter": {"current": 0.0, "set": 0.0}}
        
        table_frame = ctk.CTkFrame(self, fg_color=BG_MED, corner_radius=8)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Header
        ctk.CTkLabel(table_frame, text="Parameter Status",
                   font=("Roboto Mono", 16, "bold"),
                   text_color=HEADER_COLOR).grid(row=0, column=0, columnspan=3, pady=5)

        # Table Headers
        headers = ["Parameter", "Current", "Set Value"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(table_frame, text=header,
                       font=("Roboto Mono", 14, "bold"),
                       text_color=HEADER_COLOR).grid(row=1, column=col, padx=15, pady=3)

        # Dynamic Rows
        self.status_labels = {}
        for row, (param, values) in enumerate(self.status_data.items(), start=2):
            ctk.CTkLabel(table_frame, text=param,
                       font=("Roboto Mono", 14),
                       text_color=LABEL_COLOR).grid(row=row, column=0, sticky="w", padx=15)
            
            current_color = CURRENT_OK_COLOR if values["current"] == values["set"] else CURRENT_WARN_COLOR
            self.status_labels[param] = {
                "current": ctk.CTkLabel(table_frame, text=f"{values['current']:.2f}",
                                      font=("Roboto Mono", 14),
                                      text_color=current_color),
                "set": ctk.CTkLabel(table_frame, text=f"{values['set']:.2f}",
                                  font=("Roboto Mono", 14),
                                  text_color=SET_COLOR)
            }
            self.status_labels[param]["current"].grid(row=row, column=1, padx=15)
            self.status_labels[param]["set"].grid(row=row, column=2, padx=15)

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
            "pH": {"current": 6.8, "set": 7.0},
            "Buffer": {"current": 250, "set": 300}
        }
        super().__init__(parent, controller)

class DOFrame(ParameterFrame):
    def __init__(self, parent, controller):
        self.status_data = {
            "Dissolved O₂": {"current": 98.4, "set": 95.0},
            "O₂ Flow": {"current": 2.5, "set": 2.8}
        }
        super().__init__(parent, controller)

class ODFrame(ParameterFrame):
    def __init__(self, parent, controller):
        self.status_data = {
            "Optical Density": {"current": 0.42, "set": 0.50}
        }
        super().__init__(parent, controller)

class TempFrame(ParameterFrame):
    def __init__(self, parent, controller):
        self.status_data = {
            "Temperature": {"current": 37.2, "set": 37.0}
        }
        super().__init__(parent, controller)

class StirringFrame(ParameterFrame):
    def __init__(self, parent, controller):
        self.status_data = {
            "Stir Speed": {"current": 300, "set": 350}
        }
        super().__init__(parent, controller)

class FlowFrame(ParameterFrame):
    def __init__(self, parent, controller):
        self.status_data = {
            "Flow Rate": {"current": 2.0, "set": 2.5}
        }
        super().__init__(parent, controller)

class SetupFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_DARK)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._create_pump_assignment_ui()

    def _create_pump_assignment_ui(self):
        main_frame = ctk.CTkFrame(self, fg_color=BG_MED, corner_radius=8)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(main_frame, text="Pump Configuration",
                   font=("Roboto Mono", 16, "bold"),
                   text_color=HEADER_COLOR).pack(pady=10)

        chemicals = ["HCl", "NaOH", "Media", "Buffer", "Waste"]
        
        for pump in self.controller.pump_assignments:
            row_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=5, padx=20)
            
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

if __name__ == "__main__":
    app = App()
    app.mainloop()
