import time
import board
import busio
import tkinter as tk
import matplotlib
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from collections import deque

matplotlib.use('TkAgg')  # Set matplotlib backend to Tkinter

class BioreactorMonitor:
    def __init__(self, master):
        self.master = master
        master.title("Bioreactor Monitoring System")
        
        # Initialize hardware
        self.ads_devices = self.initialize_ads1115()
        self.channels = self.create_analog_channels()
        
        # Configure data buffers
        self.buffer_size = 100  # Data points to show
        self.x_data = deque(maxlen=self.buffer_size)
        self.y_data = [deque(maxlen=self.buffer_size) for _ in range(12)]
        
        # Create GUI layout
        self.create_control_panel()
        self.create_plots()
        
        # Start data collection
        self.running = True
        self.update_interval = 300  # ms
        self.collect_data()

    def initialize_ads1115(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        addresses = [0x48, 0x4A, 0x4B]
        devices = []
        
        for addr in addresses:
            try:
                ads = ADS.ADS1115(i2c, address=addr)
                ads.gain = 1  # ±4.096V range
                devices.append(ads)
                print(f"Initialized ADS1115 at 0x{addr:02X}")
            except Exception as e:
                print(f"Failed 0x{addr:02X}: {e}")
        
        return devices

    def create_analog_channels(self):
        channels = []
        for ads in self.ads_devices:
            for pin in (ADS.P0, ADS.P1, ADS.P2, ADS.P3):
                channels.append(AnalogIn(ads, pin))
        return channels

    def create_control_panel(self):
        control_frame = tk.Frame(self.master)
        control_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.status_label = tk.Label(control_frame, text="Status: Running")
        self.status_label.pack(side=tk.LEFT)
        
        stop_btn = tk.Button(control_frame, text="Stop", command=self.stop)
        stop_btn.pack(side=tk.RIGHT)

    def create_plots(self):
        self.fig = Figure(figsize=(12, 8), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        # Configure plot
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Voltage (V)')
        self.ax.grid(True)
        
        # Create lines for all channels
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
                 '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
                 '#bcbd22', '#17becf', '#1a55FF', '#FF1493']
        self.lines = [
            self.ax.plot([], [], color=colors[i], label=f"Ch{i}")[0]
            for i in range(12)
        ]
        self.ax.legend(ncol=3)
        
        # Embed plot in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def collect_data(self):
        if not self.running:
            return
        
        # Read all channels
        timestamp = time.time()
        voltages = [chan.voltage for chan in self.channels]
        
        # Update data buffers
        self.x_data.append(timestamp)
        for i, voltage in enumerate(voltages):
            self.y_data[i].append(voltage)
        
        # Schedule next collection and update plot
        self.master.after(50, self.collect_data)
        self.update_plot()

    def update_plot(self):
        if len(self.x_data) < 2:
            return
        
        # Update all channel lines
        for i in range(12):
            self.lines[i].set_data(self.x_data, self.y_data[i])
        
        # Adjust view limits
        self.ax.relim()
        self.ax.autoscale_view(scalex=True, scaley=False)
        self.ax.set_ylim(0, 4.096)  # Fixed voltage range
        
        # Redraw canvas
        self.canvas.draw_idle()

    def stop(self):
        self.running = False
        self.status_label.config(text="Status: Stopped")
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BioreactorMonitor(root)
    root.geometry("1200x800")
    root.mainloop()
