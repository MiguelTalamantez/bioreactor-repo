import time
import board
import busio
import tkinter as tk
from collections import deque
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class BioreactorMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Bioreactor Analog Monitor")
        self.root.geometry("1200x800")
        
        # Initialize hardware
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads_devices = self.initialize_ads1115()
        self.channels = self.create_analog_channels()
        
        # Setup GUI
        self.create_canvas()
        self.create_labels()
        
        # Data storage
        self.max_points = 100
        self.time_data = deque(maxlen=self.max_points)
        self.voltage_data = [deque(maxlen=self.max_points) for _ in range(12)]
        
        # Start updates
        self.update_interval = 200  # ms
        self.update_readings()

    def initialize_ads1115(self):
        devices = []
        for addr in [0x48, 0x4A, 0x4B]:
            try:
                ads = ADS.ADS1115(self.i2c, address=addr)
                ads.gain = 1
                devices.append(ads)
                print(f"Found ADS1115 at 0x{addr:02X}")
            except ValueError:
                print(f"No device at 0x{addr:02X}")
        return devices

    def create_analog_channels(self):
        channels = []
        for ads in self.ads_devices:
            for pin in (ADS.P0, ADS.P1, ADS.P2, ADS.P3):
                channels.append(AnalogIn(ads, pin))
        return channels

    def create_canvas(self):
        self.canvas = tk.Canvas(self.root, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_labels(self):
        self.label_frame = tk.Frame(self.root)
        self.label_frame.pack(fill=tk.X)
        
        self.labels = []
        colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00',
                 '#FF00FF', '#00FFFF', '#FFA500', '#800080',
                 '#008000', '#800000', '#008080', '#000080']
        
        for i in range(12):
            lbl = tk.Label(self.label_frame, text=f"Ch{i}: 0.000V", 
                          fg=colors[i], bg='black', font=('Arial', 10))
            lbl.pack(side=tk.LEFT, padx=5)
            self.labels.append(lbl)

    def update_readings(self):
        # Read all channels
        current_time = time.time()
        voltages = []
        
        try:
            for chan in self.channels:
                voltages.append(chan.voltage)
        except Exception as e:
            print(f"Read error: {e}")
            voltages = [0] * 12  # Default to zeros on error
        
        # Update data buffers
        self.time_data.append(current_time)
        for i in range(12):
            self.voltage_data[i].append(voltages[i] if i < len(voltages) else 0)
            self.labels[i].config(text=f"Ch{i}: {voltages[i]:.3f}V")
        
        # Update graph
        self.draw_graph()
        self.root.after(self.update_interval, self.update_readings)

    def draw_graph(self):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        # Draw axes
        margin = 50
        self.canvas.create_line(margin, margin, margin, height-margin, fill='white')
        self.canvas.create_line(margin, height-margin, width-margin, height-margin, fill='white')
        
        # Calculate scaling
        time_span = max(20, max(self.time_data)-min(self.time_data)) if self.time_data else 20
        x_scale = (width - 2*margin) / time_span
        y_scale = (height - 2*margin) / 4.096
        
        # Draw all channels
        colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00',
                 '#FF00FF', '#00FFFF', '#FFA500', '#800080',
                 '#008000', '#800000', '#008080', '#000080']
        
        for ch in range(12):
            points = []
            for i, (t, v) in enumerate(zip(self.time_data, self.voltage_data[ch])):
                x = margin + (t - self.time_data[0]) * x_scale
                y = height - margin - v * y_scale
                points.extend([x, y])
            
            if len(points) > 2:
                self.canvas.create_line(*points, fill=colors[ch], width=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = BioreactorMonitor(root)
    root.mainloop()
