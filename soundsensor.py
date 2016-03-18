#!/usr/bin/env python3

# This script is part of the linkerpy collection (https://github.com/stynoo/linkerpy)
# It is tested on Linksprite's analog Sound Sensor Module
# The shield has an MCP3008 ADC Controller 

import RPi.GPIO as GPIO
import spidev
import time
from random import randint

sound_sensor = 0	# analog port A0 on the shield
led_purple = 12
led_red = 20

loop_iter=1000
sleep_time=0.9

GPIO.setmode(GPIO.BCM)
GPIO.setup(led_red,GPIO.OUT)
GPIO.setup(led_purple,GPIO.OUT)

spi = spidev.SpiDev() # create spi object
spi.open(0, 0) # open spi port 0, device (CS) 1

def readadc(adcnum):
	if adcnum >7 or adcnum <0:
		return-1
	r = spi.xfer2([1,8+adcnum <<4,0])
	adcout = ((r[1] &3) <<8)+r[2]
	return adcout

# main
try:
	while True:
		value = readadc(sound_sensor)
		print (value)
		if value > 400:
			print ("sound")
			GPIO.output(led_red,True)
		else:
			print ("silence")
			GPIO.output(led_red,False)
		time.sleep(0.001)

except KeyboardInterrupt:
	print ("Interrupted by Keyboard...")

except:
	print ("An error or exception occurred!")

finally:
	time.sleep(0.5)
	GPIO.cleanup() # this ensures a clean exit
