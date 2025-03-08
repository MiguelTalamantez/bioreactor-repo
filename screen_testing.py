import customtkinter as ctk

def main_screen():
    # Function to display the main screen
    app = ctk.CTk()
    app.title("NIMBLE")
    app.geometry("600x400")
    
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    
    header_text = ctk.CTkLabel(app, text="NIMBLE", font=("Arial", 36), text_color="#007bff")
    header_text.pack(pady=20)
    
    options_frame = ctk.CTkFrame(app)
    options_frame.pack(pady=20)
    
    stats_button = ctk.CTkButton(options_frame, text="View Bioreactor Stats", command=lambda: stats_screen(app))
    stats_button.pack(side="left", padx=10)
    
    setpoints_button = ctk.CTkButton(options_frame, text="Set Control System Setpoints", command=lambda: setpoints_screen(app))
    setpoints_button.pack(side="left", padx=10)
    
    settings_button = ctk.CTkButton(options_frame, text="Settings", command=lambda: settings_screen(app))
    settings_button.pack(side="left", padx=10)
    
    app.mainloop()

def stats_screen(main_app):
    # Function to display the stats screen
    main_app.destroy()
    stats_app = ctk.CTk()
    stats_app.title("Bioreactor Status")
    stats_app.geometry("600x400")
    
    header_text = ctk.CTkLabel(stats_app, text="Bioreactor Status", font=("Arial", 36), text_color="#007bff")
    header_text.pack(pady=20)
    
    stats_frame = ctk.CTkFrame(stats_app)
    stats_frame.pack(pady=20)
    
    # Header Row
    header_frame = ctk.CTkFrame(stats_frame)
    header_frame.pack(fill="x")
    
    measurement_text = ctk.CTkLabel(header_frame, text="Measurement", font=("Arial", 18, "bold"))
    measurement_text.pack(side="left", expand=True)
    
    value_text = ctk.CTkLabel(header_frame, text="Value", font=("Arial", 18, "bold"))
    value_text.pack(side="left", expand=True)
    
    # Temperature Row
    temp_frame = ctk.CTkFrame(stats_frame)
    temp_frame.pack(fill="x")
    
    temp_measurement_text = ctk.CTkLabel(temp_frame, text="Temperature", font=("Arial", 14))
    temp_measurement_text.pack(side="left", expand=True)
    
    temp_value_text = ctk.CTkLabel(temp_frame, text="25°C", font=("Arial", 14))
    temp_value_text.pack(side="left", expand=True)
    
    # pH Row
    ph_frame = ctk.CTkFrame(stats_frame)
    ph_frame.pack(fill="x")
    
    ph_measurement_text = ctk.CTkLabel(ph_frame, text="pH", font=("Arial", 14))
    ph_measurement_text.pack(side="left", expand=True)
    
    ph_value_text = ctk.CTkLabel(ph_frame, text="7.0", font=("Arial", 14))
    ph_value_text.pack(side="left", expand=True)
    
    # Optical Density Row
    od_frame = ctk.CTkFrame(stats_frame)
    od_frame.pack(fill="x")
    
    od_measurement_text = ctk.CTkLabel(od_frame, text="Optical Density", font=("Arial", 14))
    od_measurement_text.pack(side="left", expand=True)
    
    od_value_text = ctk.CTkLabel(od_frame, text="0.5", font=("Arial", 14))
    od_value_text.pack(side="left", expand=True)
    
    # Dissolved Oxygen Row
    do_frame = ctk.CTkFrame(stats_frame)
    do_frame.pack(fill="x")
    
    do_measurement_text = ctk.CTkLabel(do_frame, text="Dissolved Oxygen", font=("Arial", 14))
    do_measurement_text.pack(side="left", expand=True)
    
    do_value_text = ctk.CTkLabel(do_frame, text="5.0 mg/L", font=("Arial", 14))
    do_value_text.pack(side="left", expand=True)
    
    back_button = ctk.CTkButton(stats_app, text="Back", command=lambda: back_to_main(stats_app))
    back_button.pack(pady=20)
    
    stats_app.mainloop()

def setpoints_screen(main_app):
    # Function to display the setpoints screen
    main_app.destroy()
    setpoints_app = ctk.CTk()
    setpoints_app.title("Input Value")
    setpoints_app.geometry("600x400")
    
    header_text = ctk.CTkLabel(setpoints_app, text="Input Value", font=("Arial", 36), text_color="#007bff")
    header_text.pack(pady=20)
    
    setpoints_frame = ctk.CTkFrame(setpoints_app)
    setpoints_frame.pack(pady=20)
    
    # Temperature Row
    temp_frame = ctk.CTkFrame(setpoints_frame)
    temp_frame.pack(fill="x")
    
    temp_text = ctk.CTkLabel(temp_frame, text="Temperature", font=("Arial", 14))
    temp_text.pack(side="left")
    
    temp_value = 25.0
    temp_value_text = ctk.CTkLabel(temp_frame, text=f"{temp_value}°C", font=("Arial", 14))
    temp_value_text.pack(side="left", padx=10)
    
    minus_temp_button = ctk.CTkButton(temp_frame, text="-", command=lambda: update_temp(temp_value_text, -0.5))
    minus_temp_button.pack(side="left", padx=5)
    
    plus_temp_button = ctk.CTkButton(temp_frame, text="+", command=lambda: update_temp(temp_value_text, 0.5))
    plus_temp_button.pack(side="left", padx=5)
    
    # pH Row
    ph_frame = ctk.CTkFrame(setpoints_frame)
    ph_frame.pack(fill="x")
    
    ph_text = ctk.CTkLabel(ph_frame, text="pH", font=("Arial", 14))
    ph_text.pack(side="left")
    
    ph_value = 7.0
    ph_value_text = ctk.CTkLabel(ph_frame, text=f"{ph_value:.1f}", font=("Arial", 14))
    ph_value_text.pack(side="left", padx=10)
    
    minus_ph_button = ctk.CTkButton(ph_frame, text="-", command=lambda: update_ph(ph_value_text, -0.1))
    minus_ph_button.pack(side="left", padx=5)
    
    plus_ph_button = ctk.CTkButton(ph_frame, text="+", command=lambda: update_ph(ph_value_text, 0.1))
    plus_ph_button.pack(side="left", padx=5)
    
    back_button = ctk.CTkButton(setpoints_app, text="Back", command=lambda: back_to_main(setpoints_app))
    back_button.pack(pady=20)
    
    setpoints_app.mainloop()

def update_temp(temp_text, change):
    global temp_value
    temp_value += change
    temp_text.configure(text=f"{temp_value:.1f}°C")

def update_ph(ph_text, change):
    global ph_value
    ph_value += change
    ph_text.configure(text=f"{ph_value:.1f}")

def settings_screen(main_app):
    # Function to display the settings screen
    main_app.destroy()
    settings_app = ctk.CTk()
    settings_app.title("Settings")
    settings_app.geometry("600x400")
    
    header_text = ctk.CTkLabel(settings_app, text="Settings", font=("Arial", 36), text_color="#007bff")
    header_text.pack(pady=20)
    
    settings_frame = ctk.CTkFrame(settings_app)
    settings_frame.pack(pady=20)
    
    language_text = ctk.CTkLabel(settings_frame, text="Language:")
    language_text.pack()
    
    language_combo = ctk.CTkOptionMenu(settings_frame, values=["English", "Spanish", "Chinese", "Japanese"])
    language_combo.pack()
    
    font_size_text = ctk.CTkLabel(settings_frame, text="Font Size:")
    font_size_text.pack()
    
    font_size_combo = ctk.CTkOptionMenu(settings_frame, values=["Small", "Medium", "Large"])
    font_size_combo.pack()
    
    color_mode_text = ctk.CTkLabel(settings_frame, text="Color Mode:")
    color_mode_text.pack()
    
    color_mode_combo = ctk.CTkOptionMenu(settings_frame, values=["Dark Mode", "Light Mode"])
    color_mode_combo.pack()
    
    back_button = ctk.CTkButton(settings_app, text="Back", command=lambda: back_to_main(settings_app))
    back_button.pack(pady=20)
    
    settings_app.mainloop()

def back_to_main(app):
    # Function to go back to the main screen
    app.destroy()
    main_screen()

main_screen()