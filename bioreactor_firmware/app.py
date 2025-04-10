import customtkinter as ctk
from frames import MainFrame, StatsFrame, SetpointsFrame, SettingsFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NIMBLE")
        self._configure_window()
        self._initialize_variables()
        self._create_frames()

    def _configure_window(self):
        window_width = 600
        window_height = 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int((screen_width / 2) - (window_width / 2))
        center_y = int((screen_height / 2) - (window_height / 2))
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
        if not (self.is_running and not self.is_paused):
            return

        if self.remaining_time > 0:
            hours, remainder = divmod(self.remaining_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.time_remaining_str.set(time_str)
            self.remaining_time -= 1
            self.after_id = self.after(1000, self._update_timer)