# Whack a mole game using inputs:  PB1, PB2, PB3, corresponding to GPIO 23, 24, 25 respectively
#each PB shorts 3.3V to the corresponding GPIO pin (pull up)
#uses outputs: LED1, LED2, LED3, corresponding to 4, 22, 27 respectively
import RPi.GPIO as GPIO
import random
import time



GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

PB1=23
PB2=24
PB3=25

LED1=4
LED2=22
LED3=27

GPIO.setup(PB1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(PB2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(PB3,GPIO.IN,pull_up_down=GPIO.PUD_UP)

GPIO.setup(LED1,GPIO.OUT)
GPIO.setup(LED2,GPIO.OUT)
GPIO.setup(LED3,GPIO.OUT)



def PB1callback(channel):
	if (target==PB1):
		print "PB1 pressed. Correct!"
	else:
		print "Incorrect!"
	global responseTaken
	responseTaken=1
def PB2callback(channel):
	if (target==PB2):
		print "PB2 pressed. Correct!"
	else:
		print "Incorrect"
	global responseTaken
	responseTaken=1
def PB3callback(channel):
	if (target==PB3):
		print "PB3 pressed. Correct!"
	else:
		print "Incorrect"
	global responseTaken
	responseTaken=1

GPIO.add_event_detect(PB1, GPIO.FALLING,callback=PB1callback)
GPIO.add_event_detect(PB2,GPIO.FALLING,callback=PB2callback)
GPIO.add_event_detect(PB3,GPIO.FALLING,callback=PB3callback)

timeInitial=time.time()
timeNow=time.time()
responseTaken=1

def pickTarget():
	global responseTaken
	responseTaken=0
	return random.choice([PB1,PB2,PB3])


try:

	while  ((timeNow-timeInitial)<60):
		if responseTaken:
			target=pickTarget()
			print "Target is {}\r".format(target)
		else:
			pass
		#	print "Target is {}\r".format(target),
#		time.sleep(1)
		timeNow=time.time()

	print "Time's up brah"
	GPIO.cleanup()		

except KeyboardInterrupt:
	GPIO.cleanup()
GPIO.cleanup()
