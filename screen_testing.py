from guizero import App, Text, PushButton, Box

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
    
    header_text = Text(stats_app, text="Bioreactor Status", size=24, font="Arial", color="#007bff")
    
    stats_box = Box(stats_app, border=True, width="fill", align="top")
    
    stats_text = Text(stats_box, text="Temperature: 25°C\npH: 7.0\nOptical Density: 0.5\nDissolved Oxygen: 5.0 mg/L")
    
    back_button = PushButton(stats_box, text="Back", command=lambda: back_to_main(stats_app))
    
    stats_app.display()

def setpoints_screen(main_app):
    # Function to display the setpoints screen
    main_app.destroy()
    setpoints_app = App(title="Input Value", bg="#F0F0F0", height=400, width=600)
    
    header_text = Text(setpoints_app, text="Input Value", size=24, font="Arial", color="#007bff")
    
    setpoints_box = Box(setpoints_app, border=True, width="fill", align="top")
    
    setpoints_text = Text(setpoints_box, text="Setpoints:\nTemperature: 25°C\npH: 7.0")
    
    back_button = PushButton(setpoints_box, text="Back", command=lambda: back_to_main(setpoints_app))
    
    setpoints_app.display()

def settings_screen(main_app):
    # Function to display the settings screen
    main_app.destroy()
    settings_app = App(title="Settings", bg="#F0F0F0", height=400, width=600)
    
    header_text = Text(settings_app, text="Settings", size=24, font="Arial", color="#007bff")
    
    settings_box = Box(settings_app, border=True, width="fill", align="top")
    
    settings_text = Text(settings_box, text="Language: English\nFont Size: 12\nScreen Color: White")
    
    back_button = PushButton(settings_box, text="Back", command=lambda: back_to_main(settings_app))
    
    settings_app.display()

def back_to_main(app):
    # Function to go back to the main screen
    app.destroy()
    main_screen()

main_screen()