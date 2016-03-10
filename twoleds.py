import RPi.GPIO as GPIO
import time
from random import randint

led_purple = 12
led_red = 20

loop_iter=1000
sleep_time=0.9

GPIO.setmode(GPIO.BCM)
GPIO.setup(led_red,GPIO.OUT)
GPIO.setup(led_purple,GPIO.OUT)
 
print "\nLinkerPy: furiously randomized flashing of two leds...\n"
 
for loop_count in range(0, loop_iter):
	GPIO.output(led_red,randint(0,1))
	GPIO.output(led_purple,randint(0,1))
	time.sleep(0.001)

else:
	GPIO.cleanup()
