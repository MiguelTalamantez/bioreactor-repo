import customtkinter as ctk




def main_screen():
    app = ctk.CTk()
    app.title("NIMBLE")
    window_width = 600
    window_height = 400
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    center_x = int((screen_width / 2) - (window_width / 2))
    center_y = int((screen_height / 2) - (window_height / 2))
    app.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    app.resizable(False, False)
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
    # Destroy the main app window
    main_app.destroy()
    
    # Initialize the stats screen application
    stats_app = ctk.CTk()
    stats_app.title("Bioreactor Status")
    
    # Set fixed window size and center it on the screen
    window_width = 600
    window_height = 400
    screen_width = stats_app.winfo_screenwidth()
    screen_height = stats_app.winfo_screenheight()
    center_x = int((screen_width / 2) - (window_width / 2))
    center_y = int((screen_height / 2) - (window_height / 2))
    stats_app.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    stats_app.resizable(False, False)
    
    # Header text
    header_text = ctk.CTkLabel(stats_app, text="Bioreactor Status", font=("Arial", 36), text_color="#007bff")
    header_text.pack(pady=20)
    
    # Frame for the table
    stats_frame = ctk.CTkFrame(stats_app)
    stats_frame.pack(pady=20, fill="both", expand=True)
    
    # Configure grid layout for the table
    stats_frame.grid_columnconfigure(0, weight=1, uniform="column")
    stats_frame.grid_columnconfigure(1, weight=1, uniform="column")
    
    # Header Row
    header_measurement = ctk.CTkLabel(stats_frame, text="Measurement", font=("Arial", 18, "bold"))
    header_measurement.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
    
    header_value = ctk.CTkLabel(stats_frame, text="Value", font=("Arial", 18, "bold"))
    header_value.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    
    # Data Rows
    measurements = ["Temperature", "pH", "Optical Density", "Dissolved Oxygen"]
    values = ["25°C", "7.0", "0.5", "5.0 mg/L"]
    
    for i in range(len(measurements)):
        measurement_label = ctk.CTkLabel(stats_frame, text=measurements[i], font=("Arial", 14))
        measurement_label.grid(row=i+1, column=0, padx=10, pady=5, sticky="ew")
        
        value_label = ctk.CTkLabel(stats_frame, text=values[i], font=("Arial", 14))
        value_label.grid(row=i+1, column=1, padx=10, pady=5, sticky="ew")
    
    # Back button to return to main screen
    back_button = ctk.CTkButton(stats_app, text="Back", command=lambda: back_to_main(stats_app))
    back_button.pack(pady=20)
    
    # Run the application
    stats_app.mainloop()

def setpoints_screen(main_app):
    main_app.destroy()
    setpoints_app = ctk.CTk()
    setpoints_app.title("Input Value")
    window_width = 600
    window_height = 400
    screen_width = setpoints_app.winfo_screenwidth()
    screen_height = setpoints_app.winfo_screenheight()
    center_x = int((screen_width / 2) - (window_width / 2))
    center_y = int((screen_height / 2) - (window_height / 2))
    setpoints_app.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    setpoints_app.resizable(False, False)
    header_text = ctk.CTkLabel(setpoints_app, text="Input Value", font=("Arial", 36), text_color="#007bff")
    header_text.pack(pady=20)
    setpoints_frame = ctk.CTkFrame(setpoints_app)
    setpoints_frame.pack(pady=20, fill="both", expand=True)
    setpoints_frame.grid_columnconfigure(0, weight=1, uniform="column")
    setpoints_frame.grid_columnconfigure(1, weight=1, uniform="column")
    setpoints_frame.grid_columnconfigure(2, weight=1, uniform="column")
    setpoints_frame.grid_columnconfigure(3, weight=1, uniform="column")
    temp_label = ctk.CTkLabel(setpoints_frame, text="Temperature", font=("Arial", 14))
    temp_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    temp_value = 25.0
    temp_value_label = ctk.CTkLabel(setpoints_frame, text=f"{temp_value}°C", font=("Arial", 14))
    temp_value_label.grid(row=0, column=1, padx=10, pady=10)
    minus_temp_button = ctk.CTkButton(setpoints_frame, text="-", command=lambda: update_temp(temp_value_label, -0.5))
    minus_temp_button.grid(row=0, column=2, padx=5, pady=10)
    plus_temp_button = ctk.CTkButton(setpoints_frame, text="+", command=lambda: update_temp(temp_value_label, 0.5))
    plus_temp_button.grid(row=0, column=3, padx=5, pady=10)
    ph_label = ctk.CTkLabel(setpoints_frame, text="pH", font=("Arial", 14))
    ph_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    ph_value = 7.0
    ph_value_label = ctk.CTkLabel(setpoints_frame, text=f"{ph_value:.1f}", font=("Arial", 14))
    ph_value_label.grid(row=1, column=1, padx=10, pady=10)
    minus_ph_button = ctk.CTkButton(setpoints_frame, text="-", command=lambda: update_ph(ph_value_label, -0.1))
    minus_ph_button.grid(row=1, column=2, padx=5, pady=10)
    plus_ph_button = ctk.CTkButton(setpoints_frame, text="+", command=lambda: update_ph(ph_value_label, 0.1))
    plus_ph_button.grid(row=1, column=3, padx=5, pady=10)
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
    main_app.destroy()
    settings_app=ctk.CTk()
    settings_app.title("Settings")
    window_width=600
    window_height=400
    screen_width=settings_app.winfo_screenwidth()
    screen_height=settings_app.winfo_screenheight()
    center_x=int((screen_width/2)-(window_width/2))
    center_y=int((screen_height/2)-(window_height/2))
    settings_app.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    settings_app.resizable(False,False)
    header_text=ctk.CTkLabel(settings_app,text="Settings",font=("Arial",36),text_color="#007bff")
    header_text.pack(pady=20)
    settings_frame=ctk.CTkFrame(settings_app)
    settings_frame.pack(pady=20)
    language_text=ctk.CTkLabel(settings_frame,text="Language:")
    language_text.pack()
    language_combo=ctk.CTkOptionMenu(settings_frame,values=["English","Spanish","Chinese","Japanese"])
    language_combo.pack()
    font_size_text=ctk.CTkLabel(settings_frame,text="Font Size:")
    font_size_text.pack()
    font_size_combo=ctk.CTkOptionMenu(settings_frame,values=["Small","Medium","Large"])
    font_size_combo.pack()
    color_mode_text=ctk.CTkLabel(settings_frame,text="Color Mode:")
    color_mode_text.pack()
    color_mode_combo=ctk.CTkOptionMenu(settings_frame,values=["Dark Mode","Light Mode"])
    color_mode_combo.pack()
    back_button=ctk.CTkButton(settings_app,text="Back",command=lambda:back_to_main(settings_app))
    back_button.pack(pady=20)
    settings_app.mainloop()

def back_to_main(app):
    # Function to go back to the main screen
    app.destroy()
    main_screen()

main_screen()