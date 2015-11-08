import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


GREEN_LED=18
GPIO.setup(GREEN_LED,GPIO.OUT)
LED_DELAY=2


State=0

while True:

	if State==0:
		GPIO.output(GREEN_LED,False)
		State=1
	else:
		GPIO.output(GREEN_LED,True)
		State=0

	sleep(LED_DELAY)
GPIO.cleanup()
