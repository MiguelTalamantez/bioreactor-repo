import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from collections import deque
import logging

# Configure logging
logging.basicConfig(filename='bioreactor_errors.log', level=logging.ERROR)

# Set up I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize three ADS1115 devices (update addresses if needed)
ads1 = ADS.ADS1115(i2c, address=0x48)  
ads2 = ADS.ADS1115(i2c, address=0x4A)
ads3 = ADS.ADS1115(i2c, address=0x4B)  
ads1.gain = ads2.gain = ads3.gain = 1  # ±4.096V range for all

# Initialize all 12 input channels (4 per ADS1115)
channels = [
    AnalogIn(ads1, ADS.P0), AnalogIn(ads1, ADS.P1), AnalogIn(ads1, ADS.P2), AnalogIn(ads1, ADS.P3),
    AnalogIn(ads2, ADS.P0), AnalogIn(ads2, ADS.P1), AnalogIn(ads2, ADS.P2), AnalogIn(ads2, ADS.P3),
    AnalogIn(ads3, ADS.P0), AnalogIn(ads3, ADS.P1), AnalogIn(ads3, ADS.P2), AnalogIn(ads3, ADS.P3)  # New channels
]

# Oscilloscope settings
MAX_DATA_POINTS = 50
update_interval = 500  # Increased for stability

class MultiChannelOscilloscope:
    def __init__(self, master):
        self.master = master
        self.master.title("Bioreactor Monitoring System v3.0")

        # Create voltage display frame
        self.label_frame = tk.Frame(master)
        self.label_frame.pack(pady=10)
        
        # Initialize voltage display variables (12 channels)
        self.voltage_vars = [tk.StringVar() for _ in range(12)]
        colors = ['#0000FF', '#009900', '#FF0000', '#990099',
                 '#FFA500', '#00FFFF', '#FF00FF', '#A52A2A',
                 '#808000', '#00FF00', '#800080', '#008080']  # Added 4 colors
        
        # Create three rows of labels
        for i in range(12):
            self.voltage_vars[i].set(f"Ch{i}: -- V")
            lbl = tk.Label(
                self.label_frame,
                textvariable=self.voltage_vars[i],
                font=("Arial", 12),
                fg=colors[i]
            )
            row = i // 4  # 3 rows of 4 channels each
            col = i % 4
            lbl.grid(row=row, column=col, padx=10, pady=5)

        # Data buffers
        self.x_data = [deque(maxlen=MAX_DATA_POINTS) for _ in range(12)]
        self.y_data = [deque(maxlen=MAX_DATA_POINTS) for _ in range(12)]
        self.time_offset = time.monotonic()

        # Plot setup
        self.fig = Figure(figsize=(10, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylim(0, 4.096)
        self.ax.set_xlim(0, 10)
        self.ax.grid(True)

        # Create plot lines with 12 colors
        line_colors = ['blue', 'green', 'red', 'purple',
                      'orange', 'cyan', 'magenta', 'brown',
                      'olive', 'lime', 'fuchsia', 'teal']  # Extended palette
        self.lines = [
            self.ax.plot([], [], c=color, label=f'Sensor {i}')[0]
            for i, color in enumerate(line_colors)
        ]
        self.ax.legend(loc='upper right', ncols=3)  # Adjusted to 3 columns

        # Canvas setup
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Start updates
        self.update_plot()

    def reset_ads(self):
        global i2c, ads1, ads2, ads3, channels
        
        try:
            i2c.deinit()
            time.sleep(0.5)  # Longer delay for hardware reset
            i2c = busio.I2C(board.SCL, board.SDA)
            
            ads1 = ADS.ADS1115(i2c, address=0x4A)
            ads2 = ADS.ADS1115(i2c, address=0x4B)
            ads3 = ADS.ADS1115(i2c, address=0x49)  # New device
            ads1.gain = ads2.gain = ads3.gain = 1
            
            channels = [
                AnalogIn(ads1, ADS.P0), AnalogIn(ads1, ADS.P1), AnalogIn(ads1, ADS.P2), AnalogIn(ads1, ADS.P3),
                AnalogIn(ads2, ADS.P0), AnalogIn(ads2, ADS.P1), AnalogIn(ads2, ADS.P2), AnalogIn(ads2, ADS.P3),
                AnalogIn(ads3, ADS.P0), AnalogIn(ads3, ADS.P1), AnalogIn(ads3, ADS.P2), AnalogIn(ads3, ADS.P3)
            ]
            
            self.time_offset = time.monotonic()
            logging.info("ADS1115s reset successfully")
            
        except Exception as e:
            logging.critical(f"Critical reset failure: {str(e)}")
            raise

    def update_plot(self):
        current_time = time.monotonic() - self.time_offset
        
        try:
            for i, chan in enumerate(channels):
                voltage = chan.voltage
                self.x_data[i].append(current_time)
                self.y_data[i].append(voltage)
                self.voltage_vars[i].set(f"Ch{i}: {voltage:.3f} V")
                self.lines[i].set_data(self.x_data[i], self.y_data[i])

            # Viewport adjustment
            if current_time > self.ax.get_xlim()[1]:
                self.ax.set_xlim(current_time - 10, current_time)
            
            self.canvas.draw()
            
        except OSError as e:
            logging.error(f"I2C error: {str(e)}")
            self.reset_ads()
            
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            raise
            
        finally:
            self.master.after(update_interval, self.update_plot)

# Create and run application
if __name__ == "__main__":
    root = tk.Tk()
    app = MultiChannelOscilloscope(root)
    root.geometry("1000x800")
    root.mainloop()
