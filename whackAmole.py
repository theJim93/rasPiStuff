
import RPi.GPIO as GPIO
import random

GPIO.setmode(GPIO.BCM)

PB1=23
PB2=24
PB3=25

LED1=4
LED2=27
LED3=22

GPIO.setup(PB1,GPIO.IN)
GPIO.setup(PB2,GPIO.IN)
GPIO.setup(PB3,GPIO.IN)

GPIO.setup(LED1,GPIO.OUT)
GPIO.setup(LED2,GPIO.OUT)
GPIO.setup(LED3,GPIO.OUT)


timeInitial=time.time()
timeNow=time.time()

try:

	if  ((timeNow-timeInitial)>60)):
		pickTarget=random.randInt(0,100)
		if (pickTarget<33):
			target=PB1
		elif (pickTarget>65):
			target=PB2
		else:
			target=PB3
		

		timeNow=time.time()
	else:
		GPIO.cleanup()		

except KeyboardInterrupt:
	GPIO.cleanup()
GPIO.cleanup()
