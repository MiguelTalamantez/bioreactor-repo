import time
import board
import busio
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from collections import deque

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize ADS1115 devices
ads_devices = []
for address in [0x48, 0x4A, 0x4B]:
    try:
        ads = ADS.ADS1115(i2c, address=address)
        ads.gain = 1
        ads_devices.append(ads)
    except:
        print(f"Couldn't find device at 0x{address:02X}")

# Create all 12 channels (4 per device)
channels = []
for ads in ads_devices:
    for pin in [ADS.P0, ADS.P1, ADS.P2, ADS.P3]:
        channels.append(AnalogIn(ads, pin))

# Set up plot
plt.style.use('dark_background')
fig, ax = plt.subplots()
ax.set_ylim(0, 4.096)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Voltage (V)')

# Data buffers
max_points = 50
times = deque(maxlen=max_points)
data = [deque(maxlen=max_points) for _ in range(12)]
lines = [ax.plot([], [], label=f'Ch{i}')[0] for i in range(12)]

# Add legend
ax.legend(loc='upper right', ncol=3)

def update(frame):
    # Read all channels
    voltages = [chan.voltage for chan in channels]
    current_time = time.monotonic()
    
    # Update data buffers
    times.append(current_time)
    for i, voltage in enumerate(voltages):
        data[i].append(voltage)
    
    # Update plot lines
    for i, line in enumerate(lines):
        line.set_data(times, data[i])
    
    # Adjust view limits
    ax.set_xlim(max(0, current_time-10), current_time)
    
    return lines

# Start animation
ani = FuncAnimation(fig, update, interval=200, blit=True)
plt.show()
