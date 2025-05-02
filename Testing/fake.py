import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# UI colors
BG_DARK = "#1a1a1a"
BG_MED = "#2b2b2b"
CULTURE_COLOR = "#A569BD"   # purple
SUBSTRATE_COLOR = "#EC407A" # pink/red
SET_COLOR = "#5DADE2"  # blue for other measurements

class BioreactorDataSimulator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Bioreactor Data Simulator")
        self.geometry("800x500")
        self.configure(fg_color=BG_DARK)
        ctk.set_appearance_mode("dark")
        
        # Create frames
        self.button_frame = ctk.CTkFrame(self, fg_color=BG_MED, corner_radius=8)
        self.button_frame.pack(side="top", fill="x", padx=10, pady=10)
        
        self.graph_frame = ctk.CTkFrame(self, fg_color=BG_MED, corner_radius=8)
        self.graph_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        
        # Create buttons
        self.create_buttons()
        
        # Initialize plot area
        self.fig = Figure(figsize=(6, 4), dpi=100, facecolor=BG_MED)
        self.ax = self.fig.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        # Show optical density data by default
        self.show_od_data()
    
    def create_buttons(self):
        button_props = {
            "height": 40,
            "font": ("Roboto Mono", 14),
            "corner_radius": 8,
            "fg_color": "#404040",
            "text_color": "white",
            "hover_color": "#505050"
        }
        
        self.temp_btn = ctk.CTkButton(
            self.button_frame, 
            text="Temperature", 
            command=self.show_temperature_data,
            **button_props
        )
        self.temp_btn.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
        self.od_btn = ctk.CTkButton(
            self.button_frame, 
            text="Optical Density", 
            command=self.show_od_data,
            **button_props
        )
        self.od_btn.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
        self.do_btn = ctk.CTkButton(
            self.button_frame, 
            text="Dissolved Oxygen", 
            command=self.show_do_data,
            **button_props
        )
        self.do_btn.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
        self.ph_btn = ctk.CTkButton(
            self.button_frame, 
            text="pH", 
            command=self.show_ph_data,
            **button_props
        )
        self.ph_btn.pack(side="left", padx=10, pady=10, expand=True, fill="x")
    
    def style_plot(self):
        """Apply styling to match reference image"""
        self.ax.set_facecolor(BG_DARK)
        
        # Configure axes
        self.ax.tick_params(axis='x', colors='white', labelsize=10)
        self.ax.set_yticks([])  # No y-ticks as in reference
        self.ax.set_xlabel('time', color='white', fontsize=12)
        
        # Set vertical grid lines only
        self.ax.grid(False)
        for i in range(11):
            self.ax.axvline(x=i, color='white', alpha=0.2, linewidth=1)
        
        # Style the spines
        for spine in self.ax.spines.values():
            spine.set_color('white')
        
        # Set x-axis limits
        self.ax.set_xlim(0, 10)
    
    def generate_messy_data(self, base_function, time_points, noise_level=0.05, 
                          num_spikes=10, spike_height=0.2):
        """Generate messy data that looks realistic"""
        # Base trend
        y_data = base_function(time_points)
        
        # Add noise - high frequency
        noise = noise_level * np.random.randn(len(time_points))
        
        # Add spikes - frequent and irregular
        spikes = np.zeros(len(time_points))
        if num_spikes > 0:
            spike_indices = np.random.choice(len(time_points), size=num_spikes, replace=False)
            spikes[spike_indices] = np.random.uniform(0, spike_height, size=num_spikes)
        
        # Add small oscillations at higher frequency
        high_freq = 30 * time_points
        oscillations = noise_level * 0.5 * np.sin(high_freq)
        
        # Combine everything
        final_data = y_data + noise + spikes + oscillations
        return np.clip(final_data, 0, None)  # Ensure non-negative
    
    def show_temperature_data(self):
        self.ax.clear()
        
        # Generate time points (10 hours of data)
        time = np.linspace(0, 10, 200)
        
        # Base temperature function - starts at room temp, rises to 37°C
        def temp_function(t):
            return 25 + 12 * (1 - np.exp(-t/2))
        
        # Generate temperature data
        temp_data = self.generate_messy_data(
            temp_function, time, 
            noise_level=0.3, 
            num_spikes=8, 
            spike_height=1.0
        )
        
        # Plot
        self.ax.plot(time, temp_data, color=SET_COLOR, linewidth=2)
        
        # Style to match reference
        self.style_plot()
        
        # Add custom y-axis label on left side
        self.ax.set_ylabel('temperature', color=SET_COLOR, fontsize=12)
        
        self.canvas.draw()
    
    def show_od_data(self):
        self.ax.clear()
        
        # Generate time points
        time = np.linspace(0, 10, 200)
        
        # Base functions matching the reference image patterns
        def culture_growth(t):
            # Starts low, rises during growth phase, then falls
            return 0.05 + 0.5 * (1 - np.exp(-1.2 * np.maximum(0, t-2))) * np.exp(-0.3 * np.maximum(0, t-6))
        
        def substrate_conc(t):
            # Starts high, drops over time
            return 0.9 * np.exp(-0.3 * t) + 0.1
        
        # Generate very messy data to match reference image
        culture_data = self.generate_messy_data(
            culture_growth, time, 
            noise_level=0.08, 
            num_spikes=15, 
            spike_height=0.15
        )
        
        substrate_data = self.generate_messy_data(
            substrate_conc, time, 
            noise_level=0.06, 
            num_spikes=12, 
            spike_height=0.15
        )
        
        # Plot both curves exactly matching the reference image
        self.ax.plot(time, culture_data, color=CULTURE_COLOR, linewidth=2, label="culture growth rate")
        self.ax.plot(time, substrate_data, color=SUBSTRATE_COLOR, linewidth=2, label="substrate concentration")
        
        # Style to match reference
        self.style_plot()
        
        # Add legend in top-right like reference image
        legend = self.ax.legend(loc="upper right", facecolor=BG_DARK, edgecolor="none", 
                               fontsize=10, labelcolor='white')
        
        # Add y-axis labels on sides as in reference image
        ax2 = self.ax.twinx()
        ax2.set_yticks([])
        ax2.set_ylabel("substrate concentration", color=SUBSTRATE_COLOR, 
                      fontsize=10, rotation=270, labelpad=15)
        for spine in ax2.spines.values():
            spine.set_color('white')
            
        self.ax.set_ylabel("culture growth rate", color=CULTURE_COLOR, fontsize=10)
        
        self.canvas.draw()
    
    def show_do_data(self):
        self.ax.clear()
        
        # Generate time points
        time = np.linspace(0, 10, 200)
        
        # Base DO function - starts high, drops during growth, then stabilizes
        def do_function(t):
            return 90 - 50 / (1 + np.exp(-1.5 * (t - 5))) + 20 * np.exp(-0.6 * t)
        
        # Generate DO data - match messiness of reference
        do_data = self.generate_messy_data(
            do_function, time, 
            noise_level=2.0, 
            num_spikes=18, 
            spike_height=5
        )
        
        # Plot
        self.ax.plot(time, do_data, color=SET_COLOR, linewidth=2)
        
        # Style to match reference
        self.style_plot()
        
        # Add custom y-axis label
        self.ax.set_ylabel('dissolved oxygen', color=SET_COLOR, fontsize=12)
        
        self.canvas.draw()
    
    def show_ph_data(self):
        self.ax.clear()
        
        # Generate time points
        time = np.linspace(0, 10, 200)
        
        # Base pH function - starts neutral, drops, then control system stabilizes
        def ph_function(t):
            return 7.0 - 0.8 / (1 + np.exp(-1.8 * (t - 3))) + 0.5 / (1 + np.exp(-2 * (t - 6)))
        
        # Generate pH data - match messiness of reference
        ph_data = self.generate_messy_data(
            ph_function, time, 
            noise_level=0.12, 
            num_spikes=20, 
            spike_height=0.3
        )
        
        # Plot
        self.ax.plot(time, ph_data, color=SET_COLOR, linewidth=2)
        
        # Style to match reference
        self.style_plot()
        
        # Add custom y-axis label
        self.ax.set_ylabel('pH', color=SET_COLOR, fontsize=12)
        
        self.canvas.draw()

if __name__ == "__main__":
    app = BioreactorDataSimulator()
    app.mainloop()
