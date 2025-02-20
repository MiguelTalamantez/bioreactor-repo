import time
import RPi.GPIO as GPIO


##Pin Definitions
Agitator_motor = 0
Heating_pad = 0


##Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(Agitator_motor, GPIO.OUT)
GPIO.setup(heating_pad, GPIO.OUT)



