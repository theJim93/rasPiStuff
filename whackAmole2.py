#Starting over with whackamole trying using polling instead
#each PB shorts to 3.3V when pressed (pull up) 4,18,22
#uses outputs: LED1,LED2,LED3, corresponding to GPIO 23,24,25

import RPi.GPIO as GPIO
import random
import time



GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

PB1=4
PB2=18
PB3=22
wrongLED=17

LED1=23
LED2=24
LED3=25

GPIO.setup(PB1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(PB2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(PB3,GPIO.IN,pull_up_down=GPIO.PUD_UP)

GPIO.setup(LED1,GPIO.OUT,initial=0)
GPIO.setup(LED2,GPIO.OUT,initial=0)
GPIO.setup(LED3,GPIO.OUT,initial=0)
GPIO.setup(wrongLED,GPIO.OUT,initial=0)

def blink(LED,times,pause):
	i=0
	while(i<(times+1)):
		GPIO.output(LED,1)
		time.sleep(pause)
		GPIO.output(LED,0)
		time.sleep(pause)
		i=i+1
def pickTarget():
        global responseTaken
        responseTaken=0
	chosenTarget=random.choice([LED1,LED2,LED3]) #pick LED "mole" target
#Look for the corresponding button press
	if (chosenTarget==LED1):
		chosenButton=PB1
	elif (chosenTarget==LED2):
		chosenButton=PB2
	else:
		chosenButton=PB3
        return (chosenTarget,chosenButton)

timeInitial=time.time()
timeNow=time.time()
responseTaken=1
score=0

try:
	timeLimit=(10*(1/(score+10))+0.5) #sets a time limit for the user to respond based on how well they're doing
	print timeLimit
	while((timeNow-timeInitial)<30):
		timeNow=time.time()
		if responseTaken:
			target,targetButton=pickTarget()
			print target
		else:
			tEnter=time.time()
			tLoop=time.time()
			while(((tLoop-tEnter)<timeLimit)and GPIO.input(targetButton)): #creates a short timer, only stays on while button is unpressed
				GPIO.output(target,1) #light up target
				tLoop=time.time()#update time
			if(GPIO.input(targetButton)):
				blink(wrongLED,3,0.025)
			else:
				score=score+10
				blink(target,2,0.05)
			responseTaken=1 #turn back on token
			GPIO.output(target,0)#turn off target after done
			print "\nScore:%d" % score
	print "Time's up brah\n"
except KeyboardInterrupt:
	GPIO.cleanup()
GPIO.cleanup()
