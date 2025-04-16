import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from collections import deque

# Set up ADC
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P0)

# Oscilloscope settings
MAX_DATA_POINTS = 50  # Number of points to display
update_interval = 200  # Milliseconds

class Oscilloscope:
    def __init__(self, master):
        self.master = master
        self.master.title("Raspberry Pi Oscilloscope")
        
        # Initialize data buffers
        self.x_data = deque(maxlen=MAX_DATA_POINTS)
        self.y_data = deque(maxlen=MAX_DATA_POINTS)
        self.time_offset = time.monotonic()
        
        # Create figure and axis
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylim(0, 3.3)  # Adjust based on your ADC reference voltage
        self.ax.set_xlim(0, 10)   # Initial 10-second window
        self.ax.grid(True)
        self.line, = self.ax.plot([], [], 'b-')
        
        # Set up labels
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Voltage (V)')
        self.ax.set_title('Real-time ADC Measurement')
        
        # Create Tkinter canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        # Start updates
        self.update_plot()

    def update_plot(self):
        # Read ADC value
        voltage = chan.voltage
        current_time = time.monotonic() - self.time_offset
        
        # Update data buffers
        self.x_data.append(current_time)
        self.y_data.append(voltage)
        
        # Update plot data
        self.line.set_data(self.x_data, self.y_data)
        
        # Adjust x-axis limits for scrolling effect
        if current_time > self.ax.get_xlim()[1]:
            self.ax.set_xlim(current_time - 10, current_time)
        
        # Redraw the canvas
        self.canvas.draw()
        
        # Schedule next update
        self.master.after(update_interval, self.update_plot)

# Create and run the GUI
root = tk.Tk()
app = Oscilloscope(root)
root.mainloop()
