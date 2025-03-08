from guizero import App, Text, PushButton, Box, Combo

def main_screen():
    # Function to display the main screen
    app = App(title="NIMBLE", bg="#F0F0F0", height=400, width=600)
    
    header_text = Text(app, text="NIMBLE", size=24, font="Arial", color="#007bff")
    
    options_box = Box(app, border=True, width="fill", align="top", layout="grid")
    
    stats_button = PushButton(options_box, text="View Bioreactor Stats", command=lambda: stats_screen(app), grid=[0,0], width=20, height=3)
    setpoints_button = PushButton(options_box, text="Set Control System Setpoints", command=lambda: setpoints_screen(app), grid=[1,0], width=20, height=3)
    settings_button = PushButton(options_box, text="Settings", command=lambda: settings_screen(app), grid=[2,0], width=20, height=3)
    
    app.display()

def stats_screen(main_app):
    # Function to display the stats screen
    main_app.destroy()
    stats_app = App(title="Bioreactor Status", bg="#F0F0F0", height=400, width=600)
    
    header_text = Text(stats_app, text="Bioreactor Status", size=24, font="Arial", color="#007bff", align="top")
    
    stats_box = Box(stats_app, border=True, width="fill", align="top", layout="grid")
    
    # Header Row
    Text(stats_box, text="**Measurement**", grid=[0,0], align="center", font=("Arial", 14, "bold"))
    Text(stats_box, text="**Value**", grid=[1,0], align="center", font=("Arial", 14, "bold"))
    
    # Temperature Row
    Text(stats_box, text="Temperature", grid=[0,1], align="center")
    Text(stats_box, text="25°C", grid=[1,1], align="center")
    
    # pH Row
    Text(stats_box, text="pH", grid=[0,2], align="center")
    Text(stats_box, text="7.0", grid=[1,2], align="center")
    
    # Optical Density Row
    Text(stats_box, text="Optical Density", grid=[0,3], align="center")
    Text(stats_box, text="0.5", grid=[1,3], align="center")
    
    # Dissolved Oxygen Row
    Text(stats_box, text="Dissolved Oxygen", grid=[0,4], align="center")
    Text(stats_box, text="5.0 mg/L", grid=[1,4], align="center")
    
    back_button = PushButton(stats_box, text="Back", command=lambda: back_to_main(stats_app), grid=[0,5], align="left")
    
    stats_app.display()

def setpoints_screen(main_app):
    # Function to display the setpoints screen
    main_app.destroy()
    setpoints_app = App(title="Input Value", bg="#F0F0F0", height=400, width=600)
    
    header_text = Text(setpoints_app, text="Input Value", size=24, font="Arial", color="#007bff")
    
    setpoints_box = Box(setpoints_app, border=True, width="fill", align="top", layout="grid")
    
    # Temperature Row
    Text(setpoints_box, text="Temperature", grid=[0,0], align="left")
    
    temp_value = 25.0
    temp_text = Text(setpoints_box, text=f"{temp_value}°C", grid=[1,0], align="center")
    
    minus_temp_button = PushButton(setpoints_box, text="-", command=lambda: update_temp(temp_text, -0.5), grid=[2,0], width=5)
    plus_temp_button = PushButton(setpoints_box, text="+", command=lambda: update_temp(temp_text, 0.5), grid=[3,0], width=5)
    
    # pH Row
    Text(setpoints_box, text="pH", grid=[0,1], align="left")
    
    ph_value = 7.0
    ph_text = Text(setpoints_box, text=f"{ph_value:.1f}", grid=[1,1], align="center")
    
    minus_ph_button = PushButton(setpoints_box, text="-", command=lambda: update_ph(ph_text, -0.1), grid=[2,1], width=5)
    plus_ph_button = PushButton(setpoints_box, text="+", command=lambda: update_ph(ph_text, 0.1), grid=[3,1], width=5)
    
    back_button = PushButton(setpoints_box, text="Back", command=lambda: back_to_main(setpoints_app), grid=[0,2], align="left")
    
    setpoints_app.display()

def update_temp(temp_text, change):
    global temp_value
    temp_value += change
    temp_text.value = f"{temp_value:.1f}°C"

def update_ph(ph_text, change):
    global ph_value
    ph_value += change
    ph_text.value = f"{ph_value:.1f}"

def settings_screen(main_app):
    # Function to display the settings screen
    main_app.destroy()
    settings_app = App(title="Settings", bg="#F0F0F0", height=400, width=600)
    
    header_text = Text(settings_app, text="Settings", size=24, font="Arial", color="#007bff")
    
    settings_box = Box(settings_app, border=True, width="fill", align="top")
    
    language_text = Text(settings_box, text="Language:")
    language_combo = Combo(settings_box, options=["English", "Spanish", "Chinese", "Japanese"])
    
    font_size_text = Text(settings_box, text="Font Size:")
    font_size_combo = Combo(settings_box, options=["Small", "Medium", "Large"])
    
    color_mode_text = Text(settings_box, text="Color Mode:")
    color_mode_combo = Combo(settings_box, options=["Dark Mode", "Light Mode"])
    
    back_button = PushButton(settings_box, text="Back", command=lambda: back_to_main(settings_app))
    
    settings_app.display()

def back_to_main(app):
    # Function to go back to the main screen
    app.destroy()
    main_screen()

main_screen()