#uses OpenCV functions to create a cool little OS
import RPi.GPIO as GPIO
from time import sleep
from urllib2 import urlopen
import json
import datetime

GPIO.setmode(GPIO.BCM)
#assign all outputs
aux=19
SSR=20
mainRelay=21
#initialize them all to outputs with low
GPIO.setup(aux,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(SSR,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(mainRelay,GPIO.OUT,initial=GPIO.LOW)
switchState=0

#makes it easier on the typing...
def turnOn(relay):
	GPIO.output(relay,True)
def turnOff(relay):
	GPIO.output(relay,False)
#returns hours and minutes from time string
def parseTime(timeString):
	hour=timeString.split(' ')[0].split(':')[0]
	minute=timeString.split(' ')[0].split(':')[1]
	meridian=timeString.split(' ')[1]
	if meridian=='AM':
		meridianToken=0
	else:
		meridianToken=1
#	print hour
#	print minute	
	return [hour,minute,meridianToken]

def convertMilitary(meridianToken,hour):
	militaryHour=0
	if meridianToken: #token is 1 when it's PM
		militaryHour=hour+12
	return [militaryHour]

def parseTime2(timeString):
	hour=timeString.split(' ')[1].split(':')[0]
	minute=timeString.split(' ')[1].split(':')[1]
#	print hour
#	print minute
	return [hour,minute,meridianToken]

#uses softswitch sequencing: decouples mechanical and electrical switching
def softSwitch(switchState):
	if switchState==0:
		turnOn(aux)
		sleep(0.5)
		turnOn(SSR)
		sleep(0.25)
		turnOn(mainRelay)
		sleep(0.5)
		turnOff(SSR)
		sleep(0.25)
		turnOff(aux)
		switchState=1
	else:
		turnOn(aux)
		sleep(0.5)
		turnOn(SSR)
		sleep(0.25)
		turnOff(mainRelay)
		print('Main relay off!')
		sleep(0.5)
		turnOff(SSR)
		sleep(0.25)
		turnOff(aux)
		switchState=0
	return switchState


def getSunSched():
        sunSchedGetReq=urlopen('http://api.sunrise-sunset.org/json?lat='+lat+'&'+'lng='+lng+'&date=today')
        sunSchedString=sunSchedGetReq.read()
        sunSchedDecode= json.loads(sunSchedString).get('results')
        sunset=sunSchedDecode.get('sunset')
        sunrise=sunSchedDecode.get('sunrise')
        return sunrise, sunset






#switchState=softSwitch(switchState)
#sleep(3)
#print switchState
#switchState=softSwitch(switchState)
#sleep(3)

#Input Bethlhem,PA coordinates
lat='40.625931'
lng='-75.37046'

sunSched= getSunSched()
sunrise=sunSched[0]
sunset=sunSched[1]
#print 'Sun rises at '+sunrise
#print 'length is: ' + str(len(sunrise))
#print 'Sun sets at '+sunset
#print 'length is: ' + str(len(sunset))

sunriseInt=parseTime(sunrise)
print 'sunriseInt: '
print sunriseInt
sunriseHour=int(sunriseInt[0])
sunriseMinute=int(sunriseInt[1])
sunriseHour=1
sunriseInt[2]=1
sunriseHour=convertMilitary(sunriseInt[2],sunriseHour)


sunsetInt=parseTime(sunset)
print 'sunsetInt: '
print sunsetInt
sunsetHour=int(sunsetInt[0])
sunsetMinute=int(sunsetInt[1])
sunsetHour=convertMilitary(sunsetInt[2],sunsetInt)
dateCompare=[0,0] #set up array for compare loop

#need while loop to start here
while(1):
	currentDate= str(datetime.datetime.now())
	print 'currentDate: '+currentDate
	currentHour=int(currentDate.split(' ')[1].split(':')[0])
	currentMinute=int(currentDate.split(' ')[1].split(':')[1])
	rawDate=int(currentDate.split('-')[2].split(' ')[0])
	#Make date compare array
	dateCompare[1]=rawDate
	if not dateCompare[0]==dateCompare[1]: #if there is a date change, get new sunset/sunrise data
	

GPIO.cleanup()
