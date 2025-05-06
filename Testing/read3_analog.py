import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Initialize I2C bus (no timeout parameter)
i2c = busio.I2C(board.SCL, board.SDA)

# List of ADS1115 addresses (update if your hardware differs)
addresses = [0x48, 0x4A, 0x4B]

# Create ADS1115 objects for each address
ads_devices = []
for addr in addresses:
    try:
        ads = ADS.ADS1115(i2c, address=addr)
        ads.gain = 1  # ±4.096V range
        ads_devices.append(ads)
    except Exception as e:
        print(f"Failed to initialize ADS1115 at address 0x{addr:02X}: {e}")

if len(ads_devices) != 3:
    print("Warning: Not all ADS1115 devices initialized successfully.")

# Create AnalogIn channels for all 3 devices (4 channels each)
channels = []
for ads in ads_devices:
    for pin in (ADS.P0, ADS.P1, ADS.P2, ADS.P3):
        channels.append(AnalogIn(ads, pin))

print("Starting readings from 3 ADS1115 devices (12 channels)...")
print("Press Ctrl-C to stop.")

try:
    while True:
        voltages = [chan.voltage for chan in channels]
        # Format output nicely: 3 devices × 4 channels each
        for i in range(3):
            ch_voltages = voltages[i*4:(i+1)*4]
            print(f"ADS1115 @ 0x{addresses[i]:02X}: " +
                  ", ".join(f"P{ch}: {v:.4f} V" for ch, v in enumerate(ch_voltages)))
        print("-" * 60)
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Measurement stopped by user.")
