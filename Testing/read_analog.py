import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from collections import deque

# Set up I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize both ADS1115 devices
ads1 = ADS.ADS1115(i2c, address=0x4A)  # First multiplexer
ads2 = ADS.ADS1115(i2c, address=0x4B)  # Second multiplexer
ads1.gain = ads2.gain = 1  # ±4.096V range for both

# Initialize all 8 input channels (4 per ADS1115)
channels = [
    # First ADS1115 (0x4A)
    AnalogIn(ads1, ADS.P0),
    AnalogIn(ads1, ADS.P1),
    AnalogIn(ads1, ADS.P2),
    AnalogIn(ads1, ADS.P3),
    
    # Second ADS1115 (0x4B)
    AnalogIn(ads2, ADS.P0),
    AnalogIn(ads2, ADS.P1),
    AnalogIn(ads2, ADS.P2),
    AnalogIn(ads2, ADS.P3)
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
        
        # Initialize voltage display variables for 8 channels
        self.voltage_vars = [tk.StringVar() for _ in range(8)]
        self.voltage_labels = []
        colors = ['#0000FF', '#009900', '#FF0000', '#990099',
                  '#FFA500', '#00FFFF', '#FF00FF', '#A52A2A']
        
        # Create two rows of labels for better organization
        for i in range(8):
            self.voltage_vars[i].set(f"Ch{i}: -- V")
            lbl = tk.Label(
                self.label_frame,
                textvariable=self.voltage_vars[i],
                font=("Arial", 12),
                fg=colors[i]
            )
            row = 0 if i < 4 else 1
            col = i % 4
            lbl.grid(row=row, column=col, padx=10, pady=5)
            self.voltage_labels.append(lbl)

        # Initialize data buffers for all channels
        self.x_data = [deque(maxlen=MAX_DATA_POINTS) for _ in range(8)]
        self.y_data = [deque(maxlen=MAX_DATA_POINTS) for _ in range(8)]
        self.time_offset = time.monotonic()

        # Create figure and axis
        self.fig = Figure(figsize=(10, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylim(0, 4.096)  # Matches ADC gain setting
        self.ax.set_xlim(0, 10)
        self.ax.grid(True)

        # Create plot lines for each channel
        colors = ['blue', 'green', 'red', 'purple',
                  'orange', 'cyan', 'magenta', 'brown']
        self.lines = [
            self.ax.plot([], [], c=color, label=f'Sensor {i}')[0]
            for i, color in enumerate(colors)
        ]
        self.ax.legend(loc='upper right', ncols=2)

        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Start updates
        self.update_plot()
    
    def reset_ads(self):
        global ads1, ads2, channels
        # Reinitialize I2C and ADS devices
        i2c.deinit()
        time.sleep(0.1)
        i2c = busio.I2C(board.SCL, board.SDA)
        ads1 = ADS.ADS1115(i2c, address=0x4A)
        ads2 = ADS.ADS1115(i2c, address=0x4B)
        # Recreate channels list
        channels = [
            AnalogIn(ads1, ADS.P0),
            AnalogIn(ads1, ADS.P1),
            AnalogIn(ads1, ADS.P2),
            AnalogIn(ads1, ADS.P3),
            AnalogIn(ads2, ADS.P0),
            AnalogIn(ads2, ADS.P1),
            AnalogIn(ads2, ADS.P2),
            AnalogIn(ads2, ADS.P3)
        ]

def update_plot(self):
    current_time = time.monotonic() - self.time_offset
    
    for i, chan in enumerate(channels):
        try:
            voltage = chan.voltage
        except OSError:
            # Handle I2C errors by resetting the ADC connection
            print(f"I2C error on channel {i}, reinitializing...")
            self.reset_ads()
            return  # Skip this update cycle

        self.x_data[i].append(current_time)
        self.y_data[i].append(voltage)
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
root.geometry("1000x800")
root.mainloop()
