# External module imports
import RPi.GPIO as GPIO
import time
import array
import string
from random import randint 

# Pin Definitons:
led_4d7s = 26

# Humanize:
numbers=[0b00111111,0b00000110,0b01011011,0b01001111,0b01100110,0b01101101,0b01111101,0b00000111,0b01111111,0b01101111]
letters=[0b01110111,0b01111100,0b00111001,0b01011110,0b01111001,0b01110001,0b01101111,0b01110110,0b00000110,0b00011110,0b01110110,0b00111000,0b00010101,0b01010100,0b00111111,0b01110011,0b01100111,0b01010000,0b01101101,0b01111000,0b00111110,0b00011100,0b00101010,0b01110110,0b01101110,0b01011011]

# Pin Setup:
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_4d7s,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(led_4d7s+1,GPIO.OUT,initial=GPIO.LOW)

#### TM1637
def chipdelay():
	time.sleep(0.000005)

def starttm1637():
        GPIO.output(led_4d7s,True)
        GPIO.output(led_4d7s+1,True)
	chipdelay()
	GPIO.output(led_4d7s+1,False)
        GPIO.output(led_4d7s,False)
	chipdelay()

def stoptm1637():
        GPIO.output(led_4d7s,False)
        GPIO.output(led_4d7s+1,False)
	chipdelay()
        GPIO.output(led_4d7s,True)
        GPIO.output(led_4d7s+1,True)
	chipdelay()

def writeByte(data):
        for i in range(8):
                GPIO.output(led_4d7s,False)
                if (data&0x01):
                        GPIO.output(led_4d7s+1,True)
                else:
                        GPIO.output(led_4d7s+1,False)
                GPIO.output(led_4d7s,True)
                data = (data>>1)
                chipdelay()
	GPIO.output(led_4d7s,False)
	GPIO.output(led_4d7s+1,True)
	GPIO.output(led_4d7s,True)
	GPIO.setup(led_4d7s+1,GPIO.IN)
        while(GPIO.input(led_4d7s+1)):
		chipdelay()
                if(GPIO.input(led_4d7s+1)):
			GPIO.setup(led_4d7s+1,GPIO.OUT)
			GPIO.output(led_4d7s+1,False)
			GPIO.setup(led_4d7s+1,GPIO.IN)
	GPIO.setup(led_4d7s+1,GPIO.OUT)

def send4d7s(digits=[0,0,0,0], delay=0):
        starttm1637()
        writeByte(0x40)
        stoptm1637()
        starttm1637()
        writeByte(0xC0)
        for i in range(4):
                writeByte(digits[i])
        stoptm1637()
        starttm1637()
        writeByte(0x88 + 2)
        stoptm1637()
	time.sleep(delay)

def send4d7sbar(text='    '):
	mytext=list(text.lower())
	for iloop in range(len(mytext)-3):
        	starttm1637()
        	writeByte(0x40)
        	stoptm1637()
        	starttm1637()
        	writeByte(0xC0)
		for i in range(4):
			if (mytext[i+iloop] == ' '):
				writeByte(0)
			elif (mytext[i+iloop] == '!'):
				writeByte(0b00000110)
			elif (mytext[i+iloop].isdigit()):
				writeByte(numbers[int(mytext[i+iloop])])
			else:
				writeByte(letters[ord(mytext[i+iloop]) - 97])
        	stoptm1637()
        	starttm1637()
        	writeByte(0x88 + 2)
        	stoptm1637()
		time.sleep(0.4)


#main
try:
	print "start main"
	send4d7s()
#	send4d7s([numbers[0],numbers[7],0,0b00100011],5)
#	send4d7s([letters[ord('c') - 97],letters[string.lowercase.index('a')],letters[string.lowercase.index('f')],letters[string.lowercase.index('e')]],5)
	send4d7sbar('helloo!!!')
	send4d7sbar()
	send4d7sbar('abcdefghijklmnopqrstuvwxyz 1234567890')
	
 
except KeyboardInterrupt:  
	print "Interrupted by Keyboard..."  
  
except:
	print "An error or exception occurred!"  
  
finally:
	send4d7s()
	time.sleep(0.5)
	GPIO.cleanup() # this ensures a clean exit  
