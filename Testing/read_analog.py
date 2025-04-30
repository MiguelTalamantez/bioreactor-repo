import time
import board
import busio
import ADS1x15.ads1115 as ADS
from ADS1x15.analog_in import AnalogIn
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from collections import deque

# Set up ADC with all four channels
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
ads.gain = 1  # ±4.096V range

# Initialize all four input channels
channels = [
    AnalogIn(ads, ADS.P0),
    AnalogIn(ads, ADS.P1),
    AnalogIn(ads, ADS.P2),
    AnalogIn(ads, ADS.P3)
]

# Oscilloscope settings
MAX_DATA_POINTS = 50
update_interval = 200  # Milliseconds

class MultiChannelOscilloscope:
    def __init__(self, master):
        self.master = master
        self.master.title("Bioreactor Monitoring System")

        # Create voltage display frame
        self.label_frame = tk.Frame(master)
        self.label_frame.pack(pady=10)
        
        # Initialize voltage display variables
        self.voltage_vars = [tk.StringVar() for _ in range(4)]
        self.voltage_labels = []
        colors = ['#0000FF', '#009900', '#FF0000', '#990099']
        
        for i in range(4):
            self.voltage_vars[i].set(f"Ch{i}: -- V")
            lbl = tk.Label(
                self.label_frame,
                textvariable=self.voltage_vars[i],
                font=("Arial", 14),
                fg=colors[i]
            )
            lbl.grid(row=0, column=i, padx=15)
            self.voltage_labels.append(lbl)

        # Initialize data buffers for all channels
        self.x_data = [deque(maxlen=MAX_DATA_POINTS) for _ in range(4)]
        self.y_data = [deque(maxlen=MAX_DATA_POINTS) for _ in range(4)]
        self.time_offset = time.monotonic()

        # Create figure and axis
        self.fig = Figure(figsize=(8, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylim(0, 4.096)  # Matches ADC gain setting
        self.ax.set_xlim(0, 10)
        self.ax.grid(True)

        # Create plot lines for each channel
        colors = ['blue', 'green', 'red', 'purple']
        self.lines = [
            self.ax.plot([], [], c=color, label=f'Sensor {i}')[0]
            for i, color in enumerate(colors)
        ]
        self.ax.legend(loc='upper right')

        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Start updates
        self.update_plot()

    def update_plot(self):
        current_time = time.monotonic() - self.time_offset
        
        for i, chan in enumerate(channels):
            # Read and store data
            voltage = chan.voltage
            self.x_data[i].append(current_time)
            self.y_data[i].append(voltage)
            
            # Update displays
            self.voltage_vars[i].set(f"Ch{i}: {voltage:.3f} V")
            self.lines[i].set_data(self.x_data[i], self.y_data[i])

        # Adjust viewport
        if current_time > self.ax.get_xlim()[1]:
            self.ax.set_xlim(current_time - 10, current_time)
        
        # Redraw
        self.canvas.draw()
        self.master.after(update_interval, self.update_plot)

# Create and run application
root = tk.Tk()
app = MultiChannelOscilloscope(root)
root.geometry("800x600")
root.mainloop()

