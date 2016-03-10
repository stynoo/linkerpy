# External module imports
import RPi.GPIO as GPIO
import time
import array
from random import randint 

# Pin Definitons:
led_bar = 4

# Pin Setup:
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_bar,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(led_bar+1,GPIO.OUT,initial=GPIO.LOW)

#### MY9221 
ON = 0x00ff		#8-bit 1 data
SHUT = 0x0000		#8-bit 0 data
CmdMode = 0x0000	#Work on 8-bit mode

def send16bitData(data):
	clk_pin_state = False
	for i in range(16):
		if (data&0x8000):
			GPIO.output(led_bar,1)
		else:
			GPIO.output(led_bar,0)
                clk_pin_state = not clk_pin_state
                GPIO.output(led_bar+1,clk_pin_state)
		data = (data<<1)
		time.sleep(0.00001)


def latchdata():    			#latch routine for MY9221 data exchange
        data_pin_state = False
        GPIO.output(led_bar,data_pin_state)
        time.sleep(0.0003)
        for i in range(8):
                data_pin_state = not data_pin_state
                GPIO.output(led_bar,data_pin_state)
        time.sleep(0.0003)


def sendled(ledstate):
	send16bitData(CmdMode)          #set LED Bar mode
	for i in range(12):
		if (ledstate&0x0001):
			send16bitData(ON)
		else:
			send16bitData(SHUT)
		ledstate = (ledstate>>1)
	latchdata()                     #make it come into effect


def sendbar(ledstate=[0,0,0,0,0,0,0,0,0,0], delay=0):
	ledstate.extend([0,0])		#MY9221 has 12 lines, we need to add two
	send16bitData(CmdMode)          #set LED Bar mode
	for i in range(12):
		if (ledstate[i] <= 0) or (ledstate[i] >= 6):	#some input checking
			send16bitData(SHUT)
		elif (ledstate[i] == 1):
                        send16bitData(ON)
		else:
			send16bitData(ON >> ledstate[i])
	latchdata()                     #make it come into effect
	time.sleep(delay)

def tracer():
        sendbar([0,0,0,0,0,0,0,0,0,0])
        sendbar([9,0,0,0,0,0,0,0,0,0])
        sendbar([8,9,0,0,0,0,0,0,0,0])
        sendbar([7,8,9,0,0,0,0,0,0,0])
        sendbar([6,7,8,9,0,0,0,0,0,0])
        sendbar([5,6,7,8,9,0,0,0,0,0])
        sendbar([4,5,6,7,8,9,0,0,0,0])
        sendbar([3,4,5,6,7,8,9,0,0,0])
        sendbar([2,3,4,5,6,7,8,9,0,0])
        sendbar([1,2,3,4,5,6,7,8,9,0])
	sendbar([1,1,2,3,4,5,6,7,8,9])
	sendbar([1,1,1,2,3,4,5,6,7,8])
	sendbar([2,1,1,1,2,3,4,5,6,7])
	sendbar([3,2,1,1,1,2,3,4,5,6])
	sendbar([4,3,2,1,1,1,2,3,4,5])
	sendbar([5,4,3,2,1,1,1,2,3,4])
	sendbar([6,5,4,3,2,1,1,1,2,3])
	sendbar([7,6,5,4,3,2,1,1,1,2])
	sendbar([8,7,6,5,4,3,2,1,1,1])
	sendbar([9,8,7,6,5,4,3,2,1,1])
        sendbar([0,9,8,7,6,5,4,3,2,1])
        sendbar([0,0,9,8,7,6,5,4,3,2])
        sendbar([0,0,0,9,8,7,6,5,4,3])
        sendbar([0,0,0,0,9,8,7,6,5,4])
        sendbar([0,0,0,0,0,9,8,7,6,5])
        sendbar([0,0,0,0,0,0,9,8,7,6])
        sendbar([0,0,0,0,0,0,0,9,8,7])
        sendbar([0,0,0,0,0,0,0,0,9,8])
        sendbar([0,0,0,0,0,0,0,0,0,9])
        sendbar([0,0,0,0,0,0,0,0,0,0])
        sendbar([0,0,0,0,0,0,0,0,0,9])
        sendbar([0,0,0,0,0,0,0,0,9,8])
        sendbar([0,0,0,0,0,0,0,9,8,7])
        sendbar([0,0,0,0,0,0,9,8,7,6])
        sendbar([0,0,0,0,0,9,8,7,6,5])
        sendbar([0,0,0,0,9,8,7,6,5,4])
        sendbar([0,0,0,9,8,7,6,5,4,3])
        sendbar([0,0,9,8,7,6,5,4,3,2])
        sendbar([0,9,8,7,6,5,4,3,2,1])
        sendbar([9,8,7,6,5,4,3,2,1,1])
        sendbar([8,7,6,5,4,3,2,1,1,1])
        sendbar([7,6,5,4,3,2,1,1,1,2])
        sendbar([6,5,4,3,2,1,1,1,2,3])
        sendbar([5,4,3,2,1,1,1,2,3,4])
        sendbar([4,3,2,1,1,1,2,3,4,5])
        sendbar([3,2,1,1,1,2,3,4,5,6])
        sendbar([2,1,1,1,2,3,4,5,6,7])
        sendbar([1,1,1,2,3,4,5,6,7,8])
        sendbar([1,1,2,3,4,5,6,7,8,9])
        sendbar([1,2,3,4,5,6,7,8,9,0])
        sendbar([2,3,4,5,6,7,8,9,0,0])
        sendbar([3,4,5,6,7,8,9,0,0,0])
        sendbar([4,5,6,7,8,9,0,0,0,0])
        sendbar([5,6,7,8,9,0,0,0,0,0])
        sendbar([6,7,8,9,0,0,0,0,0,0])
        sendbar([7,8,9,0,0,0,0,0,0,0])
        sendbar([8,9,0,0,0,0,0,0,0,0])
        sendbar([9,0,0,0,0,0,0,0,0,0])

def kitt():
	led_delay=0.01
        sendbar([1,1,1,2,4,5,0,0,0,0],led_delay)
        sendbar([2,1,1,1,2,0,0,0,0,0],led_delay)
        sendbar([3,2,1,1,1,2,0,0,0,0],led_delay)
        sendbar([4,3,2,1,1,1,2,0,0,0],led_delay)
        sendbar([5,4,3,2,1,1,1,2,0,0],led_delay)
        sendbar([0,5,4,3,2,1,1,1,2,0],led_delay)
        sendbar([0,0,5,4,3,2,1,1,1,2],led_delay)
        sendbar([0,0,0,5,4,3,2,1,1,1],led_delay)
        sendbar([0,0,0,0,5,4,3,2,1,1],led_delay)
	sendbar([0,0,0,0,0,5,2,1,1,1],led_delay)
	sendbar([0,0,0,0,0,2,1,1,1,2],led_delay)
	sendbar([0,0,0,0,2,1,1,1,2,3],led_delay)
	sendbar([0,0,0,2,1,1,1,2,3,4],led_delay)
	sendbar([0,0,2,1,1,1,2,3,4,5],led_delay)
	sendbar([0,2,1,1,1,2,3,4,5,0],led_delay)
        sendbar([2,1,1,1,2,3,4,5,0,0],led_delay)
	sendbar([1,1,1,2,3,4,5,0,0,0],led_delay)

def scan_right():
	led_delay=0
        sendbar([1,0,0,0,0,0,0,0,0,0],led_delay)
        sendbar([0,1,0,0,0,0,0,0,0,0],led_delay)
        sendbar([0,0,1,0,0,0,0,0,0,0],led_delay)
        sendbar([0,0,0,1,0,0,0,0,0,0],led_delay)
        sendbar([0,0,0,0,1,0,0,0,0,0],led_delay)
        sendbar([0,0,0,0,0,1,0,0,0,0],led_delay)
        sendbar([0,0,0,0,0,0,1,0,0,0],led_delay)
        sendbar([0,0,0,0,0,0,0,1,0,0],led_delay)
        sendbar([0,0,0,0,0,0,0,0,1,0],led_delay)
        sendbar([0,0,0,0,0,0,0,0,0,1],led_delay)

def scan_left():
	led_delay=0
        sendbar([0,0,0,0,0,0,0,0,0,1],led_delay)
        sendbar([0,0,0,0,0,0,0,0,1,0],led_delay)
        sendbar([0,0,0,0,0,0,0,1,0,0],led_delay)
        sendbar([0,0,0,0,0,0,1,0,0,0],led_delay)
        sendbar([0,0,0,0,0,1,0,0,0,0],led_delay)
        sendbar([0,0,0,0,1,0,0,0,0,0],led_delay)
        sendbar([0,0,0,1,0,0,0,0,0,0],led_delay)
        sendbar([0,0,1,0,0,0,0,0,0,0],led_delay)
        sendbar([0,1,0,0,0,0,0,0,0,0],led_delay)
        sendbar([1,0,0,0,0,0,0,0,0,0],led_delay)

def chaos():
	sendbar([randint(0,5),randint(0,5),randint(0,5),randint(0,5),randint(0,5),randint(0,5),randint(0,5),randint(0,5),randint(0,5),randint(0,5)])

def flip():
        led_delay=0
        sendbar([1,0,1,0,1,0,1,0,1,0],led_delay)
        sendbar([0,1,0,1,0,1,0,1,0,1],led_delay)

def sparkle():
	ledstate=[0,0,0,0,0,0,0,0,0,0]
	ledstate[randint(0,9)]=randint(0,5)
	sendbar(ledstate)

def flow():
	led_delay=0.01
	sendbar([1,2,3,4,5,5,4,3,2,1],led_delay)
	sendbar([2,1,2,3,4,4,3,2,1,2],led_delay)
	sendbar([3,2,1,2,3,3,2,1,2,3],led_delay)
	sendbar([4,3,2,1,2,2,1,2,3,4],led_delay)
	sendbar([5,4,3,2,1,1,2,3,4,5],led_delay)
	sendbar([4,5,4,3,2,2,3,4,5,4],led_delay)
	sendbar([3,4,5,4,3,3,4,5,4,3],led_delay)
	sendbar([2,3,4,5,4,4,5,4,3,2],led_delay)

def fill_right():
	led_delay=0.05
	sendbar([1,0,0,0,0,0,0,0,0,0],led_delay)
	sendbar([1,1,0,0,0,0,0,0,0,0],led_delay)
	sendbar([1,1,1,0,0,0,0,0,0,0],led_delay)
	sendbar([1,1,1,1,0,0,0,0,0,0],led_delay)
	sendbar([1,1,1,1,1,0,0,0,0,0],led_delay)
	sendbar([1,1,1,1,1,1,0,0,0,0],led_delay)
	sendbar([1,1,1,1,1,1,1,0,0,0],led_delay)
	sendbar([1,1,1,1,1,1,1,1,0,0],led_delay)
	sendbar([1,1,1,1,1,1,1,1,1,0],led_delay)
	sendbar([1,1,1,1,1,1,1,1,1,1],led_delay)

#main
try:  
	sendbar()
	for loop_count in range(0, 5): fill_right()	
	for loop_count in range(0, 100): sparkle()
	for loop_count in range(0, 100): chaos()
	for loop_count in range(0, 10): flip()
	for loop_count in range(0, 5): scan_right();scan_left()
	for loop_count in range(0, 10): flow()
	for loop_count in range(0, 5): kitt()
	for loop_count in range(0, 4): tracer()
  
except KeyboardInterrupt:  
	print "Interrupted by Keyboard..."  
  
except:
	print "An error or exception occurred!"  
  
finally:
	sendbar()
	time.sleep(0.5)
	GPIO.cleanup() # this ensures a clean exit  
