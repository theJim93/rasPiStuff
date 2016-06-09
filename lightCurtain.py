import RPi.GPIO as GPIO
from time import sleep

#activity teaches about the concept of Light Curtain
#Inputs: Photo resistor tied to GPIO pin 23: 150kOhms tied to 5V, touches 1kOhm current limit resistor which goes to GPIO23, from that node PhotoResistor runs to ground. Place 5
#Outputs: Red blinking LED, piezoelectric speaker?

GPIO.setmode(GPIO.BCM)

GREEN_LED=18
GPIO.setup(GREEN_LED,GPIO.OUT)
photoRes=23
GPIO.setup(photoRes,GPIO.IN)
LED_DELAY=0.05


State=0



while True:

        while (GPIO.input(photoRes)):

                if State==0:
                        GPIO.output(GREEN_LED,False)
                        State=1
                else:
                        GPIO.output(GREEN_LED,True)
                        State=0

                sleep(LED_DELAY)
        GPIO.output(GREEN_LED,False)
