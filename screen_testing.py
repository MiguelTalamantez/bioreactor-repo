import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NIMBLE")
        window_width=600
        window_height=400
        screen_width=self.winfo_screenwidth()
        screen_height=self.winfo_screenheight()
        center_x=int((screen_width/2)-(window_width/2))
        center_y=int((screen_height/2)-(window_height/2))
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.resizable(False,False)
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.frames={}
        for F in (MainFrame,StatsFrame,SetpointsFrame,SettingsFrame):
            frame=F(self)
            self.frames[F]=frame
            frame.grid(row=0,column=0,sticky="nsew")
        self.show_frame(MainFrame)
    
    def show_frame(self,cont):
        frame=self.frames[cont]
        frame.tkraise()

class MainFrame(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        header_text=ctk.CTkLabel(self,text="NIMBLE",font=("Arial",36),text_color="#007bff")
        header_text.pack(pady=20)
        options_frame=ctk.CTkFrame(self)
        options_frame.pack(pady=20)
        ctk.CTkButton(options_frame,text="View Bioreactor Stats",command=lambda:parent.show_frame(StatsFrame)).pack(side="left",padx=10)
        ctk.CTkButton(options_frame,text="Set Control System Setpoints",command=lambda:parent.show_frame(SetpointsFrame)).pack(side="left",padx=10)
        ctk.CTkButton(options_frame,text="Settings",command=lambda:parent.show_frame(SettingsFrame)).pack(side="left",padx=10)

class StatsFrame(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        header_text=ctk.CTkLabel(self,text="Bioreactor Status",font=("Arial",36),text_color="#007bff")
        header_text.pack(pady=20)
        stats_frame=ctk.CTkFrame(self)
        stats_frame.pack(pady=20,fill="both",expand=True)
        stats_frame.grid_columnconfigure(0,weight=1,uniform="column")
        stats_frame.grid_columnconfigure(1,weight=1,uniform="column")
        ctk.CTkLabel(stats_frame,text="Measurement",font=("Arial",18,"bold")).grid(row=0,column=0,padx=10,pady=5,sticky="ew")
        ctk.CTkLabel(stats_frame,text="Value",font=("Arial",18,"bold")).grid(row=0,column=1,padx=10,pady=5,sticky="ew")
        measurements=["Temperature","pH","Optical Density","Dissolved Oxygen"]
        values=["25°C","7.0","0.5","5.0 mg/L"]
        for i in range(len(measurements)):
            ctk.CTkLabel(stats_frame,text=measurements[i],font=("Arial",14)).grid(row=i+1,column=0,padx=10,pady=5,sticky="ew")
            ctk.CTkLabel(stats_frame,text=values[i],font=("Arial",14)).grid(row=i+1,column=1,padx=10,pady=5,sticky="ew")
        ctk.CTkButton(self,text="Back",command=lambda:parent.show_frame(MainFrame)).pack(pady=20)

class SetpointsFrame(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.temp_value=25.0
        self.ph_value=7.0
        header_text=ctk.CTkLabel(self,text="Input Value",font=("Arial",36),text_color="#007bff")
        header_text.pack(pady=20)
        setpoints_frame=ctk.CTkFrame(self)
        setpoints_frame.pack(pady=20,fill="both",expand=True)
        for col in range(4):setpoints_frame.grid_columnconfigure(col,weight=1,uniform="column")
        self.create_row(setpoints_frame,"Temperature",0,self.temp_value,"°C",self.update_temp)
        self.create_row(setpoints_frame,"pH",1,self.ph_value,"",self.update_ph)
        ctk.CTkButton(self,text="Back",command=lambda:parent.show_frame(MainFrame)).pack(pady=20)
    
    def create_row(self,frame,label,row,value,unit,callback):
        ctk.CTkLabel(frame,text=label,font=("Arial",14)).grid(row=row,column=0,padx=10,pady=10,sticky="w")
        self.value_label=ctk.CTkLabel(frame,text=f"{value}{unit}",font=("Arial",14))
        self.value_label.grid(row=row,column=1,padx=10,pady=10)
        ctk.CTkButton(frame,text="-",command=lambda:callback(-0.5 if label=="Temperature" else -0.1)).grid(row=row,column=2,padx=5,pady=10)
        ctk.CTkButton(frame,text="+",command=lambda:callback(0.5 if label=="Temperature" else 0.1)).grid(row=row,column=3,padx=5,pady=10)
    
    def update_temp(self,change):
        self.temp_value+=change
        self.value_label.configure(text=f"{self.temp_value:.1f}°C")
    
    def update_ph(self,change):
        self.ph_value+=change
        self.value_label.configure(text=f"{self.ph_value:.1f}")

class SettingsFrame(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        header_text=ctk.CTkLabel(self,text="Settings",font=("Arial",36),text_color="#007bff")
        header_text.pack(pady=20)
        settings_frame=ctk.CTkFrame(self)
        settings_frame.pack(pady=20)
        ctk.CTkLabel(settings_frame,text="Language:").pack()
        ctk.CTkOptionMenu(settings_frame,values=["English","Spanish","Chinese","Japanese"]).pack()
        ctk.CTkLabel(settings_frame,text="Font Size:").pack()
        ctk.CTkOptionMenu(settings_frame,values=["Small","Medium","Large"]).pack()
        ctk.CTkLabel(settings_frame,text="Color Mode:").pack()
        ctk.CTkOptionMenu(settings_frame,values=["Dark Mode","Light Mode"]).pack()
        ctk.CTkButton(self,text="Back",command=lambda:parent.show_frame(MainFrame)).pack(pady=20)

if __name__=="__main__":
    app=App()
    app.mainloop()