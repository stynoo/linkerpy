#!/usr/bin/env python3

# This script is part of the linkerpy collection (https://github.com/stynoo/linkerpy)
# It is tested on Linksprite's 4-Digit 7-Segment Module and is driving the TM1637 chip via RPi.GPIO

# The TM1637 datasheet is available in Chineese but there it has some sample code.
# Linksprite's code examples (ccp for arduino) did help as well.

# External module imports
import RPi.GPIO as GPIO
import time
import array
import string
from random import randint 

# Pin Definitons:
led_4d7s = 26

# The chip accepts bits so we construct an array for numbers and one for the alphabet:
numbers=[0b00111111,0b00000110,0b01011011,0b01001111,0b01100110,0b01101101,0b01111101,0b00000111,0b01111111,0b01101111]
letters=[0b01110111,0b01111100,0b00111001,0b01011110,0b01111001,0b01110001,0b01101111,0b01110110,0b00000110,0b00011110,0b01110110,0b00111000,0b00010101,0b01010100,0b00111111,0b01110011,0b01100111,0b01010000,0b01101101,0b01111000,0b00111110,0b00011100,0b00101010,0b01110110,0b01101110,0b01011011]

# Pin Setup:
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_4d7s,GPIO.OUT,initial=GPIO.LOW)		# set clock
GPIO.setup(led_4d7s+1,GPIO.OUT,initial=GPIO.LOW)	# set data

def chipdelay():
	time.sleep(0.000005)

# TM1637 specific start routine:
def starttm1637():
	GPIO.output(led_4d7s,True)
	GPIO.output(led_4d7s+1,True)
	chipdelay()
	GPIO.output(led_4d7s+1,False)
	GPIO.output(led_4d7s,False)
	chipdelay()

# TM1637 specific stop routine: 
def stoptm1637():
	GPIO.output(led_4d7s,False)
	GPIO.output(led_4d7s+1,False)
	chipdelay()
	GPIO.output(led_4d7s,True)
	GPIO.output(led_4d7s+1,True)
	chipdelay()

# TM1637 specific write routine:
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

# TM1637 write routine: start|0x40|stop|start|<yourdigits>|stop|start|0x88+brightness|stop
# To illuminate the ":" on the display we need to flip the first bit to 1 (thus adding 0b10000000 when needed)
def send4d7sbar(text='    ',doublepoint=False):
	if (doublepoint):
		dpvalue=0b10000000
	else:
		dpvalue=0
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
			elif (mytext[i+iloop] == '-'):
				writeByte(0b01000000)
			elif (mytext[i+iloop].isdigit()):
				writeByte(numbers[int(mytext[i+iloop])] + dpvalue)
			else:
				writeByte(letters[ord(mytext[i+iloop]) - 97 + dpvalue])
		stoptm1637()
		starttm1637()
		writeByte(0x88 + 2)
		stoptm1637()
		time.sleep(0.4)

# main
try:
	print ("running... nothing to see here, look at the leds...")

	send4d7sbar('----')
	time.sleep(1)
	
	send4d7sbar('8888')
	send4d7sbar(' 888')
	send4d7sbar('8 88')
	send4d7sbar('88 8')
	send4d7sbar('888 ')
	send4d7sbar('8888')
	send4d7sbar('888 ')
	send4d7sbar('88 8')
	send4d7sbar('88 8')
	send4d7sbar('8 88')
	send4d7sbar(' 888')
	send4d7sbar('8888')

	send4d7sbar('12345678901234567890',True)

	send4d7sbar('abcdefghijklmnopqrstuvwxyz')

	print ("finished...")
 
except KeyboardInterrupt:  
	print ("Interrupted by Keyboard...") 
  
except:
	print ("An error or exception occurred!") 
  
finally:
	send4d7sbar()
	time.sleep(0.5)
	GPIO.cleanup() # this ensures a clean exit  
