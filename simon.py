#Simon game
#uses LED outputs: 23,24,25
#uses PB inputs:4, 18, 22
	
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

sequence=[]
answerSequence=[]
level=1

#Sets the sequence by appending to the array
def setSequence():
        global sequence
        sequence.append(random.choice([LED1,LED2,LED3]))
        return sequence

def playSequence(sequence,difficulty):
	pause=1-(0.1*difficulty)
	if (difficulty>8):
		pause=0.2
	for x in range(0,len(sequence)):
		time.sleep(pause)
		GPIO.output(sequence[x],1)
		time.sleep(pause)
		GPIO.output(sequence[x],0)
	return 0

def blink(LED,times,pause):
        i=0
        while(i<(times+1)):
                GPIO.output(LED,1)
                time.sleep(pause)
                GPIO.output(LED,0)
                time.sleep(pause)
                i=i+1

sequenceToken=1
level=1
try:
	while(1):
		if(sequenceToken): #runs before user attempt
			answerSequence=[] #empty out answerSequence
			setSequence() #append to the sequence
			playSequence(sequence,level) #turn on the corresponding lights on with corresponding difficulty
			sequenceToken=0 #flags readiness to take user input
		else: #runs while waiting for user input
			answerToken=1 #when loop starts, ensure that answerSequence can be appended
			while((GPIO.input(PB1))and(GPIO.input(PB2))and(GPIO.input(PB3))): #ensures we stay in the loop before button press
				time.sleep(0.001)
			while(GPIO.input(PB1)==0): #ensures proper LED lights up while they're pressing it and makes sure there's a one time addition to answerSequence
				if(answerToken==1):
					answerSequence.append(LED1)
					answerToken=0
				GPIO.output(LED1,1)
				time.sleep(0.2)
			GPIO.output(LED1,0)
			while(GPIO.input(PB2)==0): #same as above
				if(answerToken==1):
					answerSequence.append(LED2)
					answerToken=0
				GPIO.output(LED2,1)
				time.sleep(0.2)
			GPIO.output(LED2,0)
			while(GPIO.input(PB3)==0): #same as above
				if(answerToken==1):
					answerSequence.append(LED3)
					answerToken=0
				GPIO.output(LED3,1)
				time.sleep(0.2)
			GPIO.output(LED3,0)	
			if(answerSequence==sequence[0:len(answerSequence)]):
				sequenceToken=0 #as long as they're right so far, continue polling
				if(len(answerSequence)==len(sequence)): #if they've gotten the whole sequence right, stop polling, set up new sequence
					sequenceToken=1
					level=level+1 #means they got it right, increment difficulty
			else: #if they're wrong, go back to beginning, set a whole new sequence
				sequenceToken=1 #closes loop if they're right or finished
				sequence=[]#resets the sequence
				level=1 #resets difficulty level
				blink(wrongLED,3,0.05)
	
			time.sleep(0.1)#ensures debouncing takes place
except KeyboardInterrupt:
	GPIO.cleanup()
GPIO.cleanup()
