import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD) 
GPIO.setwarnings(False)

step1=19
dir1 = 21
step2 = 31
dir2 = 29
step3 = 40
dir3 = 37
step4 = 35
dir4 = 33

#setting up outputs
GPIO.setup(step1,GPIO.OUT)
GPIO.setup(step2,GPIO.OUT)
GPIO.setup(step3,GPIO.OUT)
GPIO.setup(step4,GPIO.OUT)
GPIO.setup(dir1,GPIO.OUT)
GPIO.setup(dir2,GPIO.OUT)
GPIO.setup(dir3,GPIO.OUT)
GPIO.setup(dir4,GPIO.OUT)

while True:
	GPIO.output(dir1,1)
	GPIO.output(dir2,0)
	GPIO.output(dir3,1)
	GPIO.output(dir4,0)
	#pulse stepper 1 [ACID]
	for i in range(200):
		GPIO.output(step1,1)
		time.sleep(0.001)
		GPIO.output(step1,0)
		time.sleep(0.001)
		print("ACID")
	print("waiting")
	time.sleep(0.5)
	#pulse stepper 2 [BASE]
	for i in range(200):
		GPIO.output(step2,1)
		time.sleep(0.001)
		GPIO.output(step2,0)
		time.sleep(0.001)
		print("BASE")
	print("waiting")
	time.sleep(0.5)
	#pulse stepper 3 [FEED]
	for i in range(200):
		GPIO.output(step3,1)
		time.sleep(0.001)
		GPIO.output(step3,0)
		time.sleep(0.001)
		print("FEED")
	print("waiting")
	time.sleep(0.5)
	#pulse stepper 4 [OUTPUT]
	for i in range(200):
		GPIO.output(step4,1)
		time.sleep(0.001)
		GPIO.output(step4,0)
		time.sleep(0.001)
		print("OUTPUT")
	print("waiting")
	time.sleep(0.5)
GPIO.cleanup()
