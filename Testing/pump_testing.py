# Port Layout
# VCC+ (red) = 12
# FG Signal (green) = GPIO 23
# CW / CCW (yellow) = GPIO 24
# GND = whatever
# PWM Speed adjusting (blue) = GPIO 12


import customtkinter as ctk
import tkinter as tk
from datetime import timedelta
import pigpio
import time

# Initialize pigpio daemon connection
pi = pigpio.pi()

# Pin assignments (BCM numbering)
DIRECTION_PIN = 24   # CW/CCW control (yellow wire)
PWM_PIN = 12         # Speed adjustment (blue wire)
FREQUENCY = 1000     # PWM frequency in Hz (adjust if needed)

# Configure pins
pi.set_mode(DIRECTION_PIN, pigpio.OUTPUT)
pi.set_PWM_frequency(PWM_PIN, FREQUENCY)

def set_pump_speed(direction, speed_percent):
    """
    Control pump direction and speed
    :param direction: 0 (CCW) or 1 (CW)
    :param speed_percent: 0-100 (duty cycle percentage)
    """
    # Set direction
    pi.write(DIRECTION_PIN, direction)
    
    # Convert percentage to 0-255 range for pigpio
    duty_cycle = int((speed_percent / 100) * 255)
    duty_cycle = max(0, min(255, duty_cycle))  # Clamp values
    
    pi.set_PWM_dutycycle(PWM_PIN, duty_cycle)

try:
    # Example usage
    set_pump_speed(direction=1, speed_percent=50)  # Forward at 50% speed
    time.sleep(5)
    
    set_pump_speed(direction=0, speed_percent=75)  # Reverse at 75% speed
    time.sleep(5)
    
    set_pump_speed(direction=1, speed_percent=0)   # Stop pump

except KeyboardInterrupt:
    print("\nStopping pump...")
finally:
    # Cleanup
    pi.set_PWM_dutycycle(PWM_PIN, 0)
    pi.stop()


