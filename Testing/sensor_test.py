import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

OD = 11
pH = 13
DO = 15

GPIO.setup(OD, GPIO.OUT)
GPIO.setup(pH, GPIO.OUT)
GPIO.setup(DO, GPIO.OUT)

try:
	while True:
		GPIO.output(OD,1)
		GPIO.output(pH,0)
		GPIO.output(DO,0)
		time.sleep(1)
		print("OD")
		GPIO.output(OD,0)
		GPIO.output(pH,1)
		GPIO.output(DO,0)
		time.sleep(1)
		print("pH")
		GPIO.output(OD,0)
		GPIO.output(pH,0)
		GPIO.output(DO,1)
		time.sleep(1)
		print("DO")

except KeyboardInterrupt:
	print("\nKeyboard interrupt detected, cleaning up")
	GPIO.output(OD,0)
	GPIO.output(pH,0)
	GPIO.output(DO,0)
	GPIO.cleanup()
	time.sleep(0.5)
