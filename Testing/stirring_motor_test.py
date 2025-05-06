import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

stir_pin = 36
GPIO.setup(stir_pin, GPIO.OUT)

pwm = GPIO.PWM(stir_pin, 60)
pwm.start(0)

try:
	while True:
		for i in range(0,70,1):
			pwm.ChangeDutyCycle(i)
			time.sleep(0.05)
			print("up")
			
		for i in range(70,0,-1):
			pwm.ChangeDutyCycle(i)
			time.sleep(0.05)
			print("down")

except KeyboardInterrupt:
	print("\nKeyboard interrupt detected, cleaning up") 
	pwm.stop()
	GPIO.cleanup()
	time.sleep(0.5)
