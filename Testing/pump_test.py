import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#Settings up outputs
#STEP
GPIO.setup(19, GPIO.OUT)
#DIR
GPIO.setup(21, GPIO.OUT)

while True:
    GPIO.output(21, 1)
    for i in range(200):
        GPIO.output(19,1)
        time.sleep(0.001) 
        GPIO.output(19,0)
        time.sleep(0.001)
        print("beep")
    pritn("waiting")
    time.sleep(0.5)
GPIO.cleanup()


        