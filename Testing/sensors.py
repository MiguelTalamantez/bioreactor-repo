# bioreactor_sensor_test_ads1115.py
import time
import board
import busio
import matplotlib.pyplot as plt
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Configuration
VREF = 4.096  # Default full-scale range with PGA=1 (adjust based on gain)
CHANNELS = 4
SAMPLE_INTERVAL = 0.5
GAIN = 1  # Programmable Gain Amplifier setting (1 = ±4.096V)

def setup_adc():
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c, gain=GAIN)
        return [AnalogIn(ads, getattr(ADS, f'P{i}')) for i in range(CHANNELS)]
    except Exception as e:
        print(f"ADC initialization failed: {e}")
        print("Check wiring and I2C enablement (raspi-config > Interface Options > I2C)")
        print("Verify ADS1115 detection with: sudo i2cdetect -y 1")
        exit(1)

def read_sensors(channels):
    return [(chan.value, chan.voltage) for chan in channels]

def display_data(readings):
    print("\n" + "-"*65)
    print(f"{'Channel':<10} | {'Raw Value':<12} | {'Voltage (V)':<12} | {'Status'}")
    print("-"*65)
    
    for i, (raw, voltage) in enumerate(readings):
        status = "OK" if 0.1 < voltage < VREF-0.1 else "CHECK SENSOR/WIRING"
        print(f"{i:<10} | {raw:<12} | {voltage:<12.4f} | {status}")

def plot_data(readings):
    plt.clf()
    voltages = [v for _, v in readings]
    plt.bar(range(CHANNELS), voltages)
    plt.ylim(0, VREF)
    plt.ylabel('Voltage (V)')
    plt.xlabel('Channel')
    plt.title(f'Bioreactor Sensor Voltages (Gain={GAIN}x)')
    plt.pause(0.05)

if __name__ == "__main__":
    print("Initializing ADS1115 bioreactor monitoring...")
    channels = setup_adc()
    
    try:
        plt.ion()
        while True:
            readings = read_sensors(channels)
            display_data(readings)
            plot_data(readings)
            time.sleep(SAMPLE_INTERVAL)
            
    except KeyboardInterrupt:
        plt.close()
        print("\nMonitoring stopped")