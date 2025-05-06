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
import sys
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='bioreactor_errors.log'
)

class BioreactorMonitor:
    def __init__(self):
        self.i2c = None
        self.ads_devices = []
        self.channels = []
        self.data_lock = threading.Lock()
        self.running = True
        self.init_ads()

    def init_ads(self, retries=3):
        """Initialize I2C and ADS1115 devices with retry logic"""
        for attempt in range(retries):
            try:
                if self.i2c:
                    self.i2c.deinit()
                
                self.i2c = busio.I2C(board.SCL, board.SDA, timeout=0.1)
                self.ads_devices = [
                    ADS.ADS1115(self.i2c, address=addr) for addr in (0x48, 0x4A, 0x4B)
                ]
                
                for ads in self.ads_devices:
                    ads.gain = 1  # ±4.096V range
                
                # Initialize all 12 channels
                self.channels = [
                    AnalogIn(ads, pin)
                    for ads in self.ads_devices
                    for pin in (ADS.P0, ADS.P1, ADS.P2, ADS.P3)
                ]
                logging.info("ADS1115s initialized successfully")
                return
                
            except (OSError, ValueError) as e:
                logging.error(f"Init attempt {attempt+1} failed: {str(e)}")
                time.sleep(1)
        
        logging.critical("ADS1115 initialization failed after retries")
        raise RuntimeError("Failed to initialize ADS1115 devices")

    def read_sensors(self):
        """Continuous sensor reading thread target"""
        while self.running:
            try:
                readings = [(time.monotonic(), chan.voltage) for chan in self.channels]
                with self.data_lock:
                    for i, (t, v) in enumerate(readings):
                        self.x_data[i].append(t - self.time_offset)
                        self.y_data[i].append(v)
            except OSError as e:
                logging.error(f"I2C read error: {str(e)}")
                self.init_ads()  # Reinitialize on bus errors
            except Exception as e:
                logging.error(f"Unexpected read error: {str(e)}")
            time.sleep(0.1)  # 100ms read interval

class MultiChannelOscilloscope:
    def __init__(self, master):
        self.master = master
        self.master.title("Bioreactor Monitoring System v3.1")
        self.monitor = BioreactorMonitor()
        
        # Initialize data structures
        self.time_offset = time.monotonic()
        self.x_data = [deque(maxlen=50) for _ in range(12)]
        self.y_data = [deque(maxlen=50) for _ in range(12)]
        
        # Start sensor thread
        self.sensor_thread = threading.Thread(
            target=self.monitor.read_sensors,
            daemon=True
        )
        self.sensor_thread.start()

        # GUI setup
        self.setup_ui()
        self.update_plot()

    def setup_ui(self):
        """Initialize all user interface components"""
        # Voltage display frame
        self.label_frame = tk.Frame(self.master)
        self.label_frame.pack(pady=10)
        
        # Voltage display variables
        self.voltage_vars = [tk.StringVar() for _ in range(12)]
        colors = ['#0000FF', '#009900', '#FF0000', '#990099',
                 '#FFA500', '#00FFFF', '#FF00FF', '#A52A2A',
                 '#808000', '#00FF00', '#800080', '#008080']
        
        # Create sensor labels
        for i in range(12):
            self.voltage_vars[i].set(f"Ch{i}: -- V")
            lbl = tk.Label(
                self.label_frame,
                textvariable=self.voltage_vars[i],
                font=("Arial", 12),
                fg=colors[i]
            )
            lbl.grid(row=i//4, column=i%4, padx=10, pady=5)

        # Plot configuration
        self.fig = Figure(figsize=(10, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylim(0, 4.096)
        self.ax.set_xlim(0, 10)
        self.ax.grid(True)
        
        # Create plot lines
        line_colors = ['blue', 'green', 'red', 'purple',
                      'orange', 'cyan', 'magenta', 'brown',
                      'olive', 'lime', 'fuchsia', 'teal']
        self.lines = [
            self.ax.plot([], [], c=color, label=f'Sensor {i}')[0]
            for i, color in enumerate(line_colors)
        ]
        self.ax.legend(loc='upper right', ncols=3)
        
        # Canvas setup
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_plot(self):
        """Update GUI elements with latest sensor data"""
        try:
            # Update voltage displays
            with self.monitor.data_lock:
                for i in range(12):
                    if self.y_data[i]:
                        self.voltage_vars[i].set(
                            f"Ch{i}: {self.y_data[i][-1]:.3f} V"
                        )
                        self.lines[i].set_data(self.x_data[i], self.y_data[i])
            
            # Adjust viewport
            current_time = time.monotonic() - self.time_offset
            if current_time > self.ax.get_xlim()[1]:
                self.ax.set_xlim(current_time - 10, current_time)
            
            self.canvas.draw()
            
        except Exception as e:
            logging.error(f"GUI update error: {str(e)}")
            
        finally:
            self.master.after(500, self.update_plot)

    def on_close(self):
        """Cleanup resources on window close"""
        self.monitor.running = False
        self.sensor_thread.join(timeout=1)
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiChannelOscilloscope(root)
    root.geometry("1000x800")
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
