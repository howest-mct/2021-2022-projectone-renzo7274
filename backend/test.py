#######     rotary encoder code    #######
import time
from RPi import GPIO


global counter
counter = 0
clkLastState = 0
switchState = 0

clk_pin = 18
dt_pin = 17
sw_pin = 27

def setup():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(clk_pin, GPIO.IN, GPIO.PUD_UP)
  GPIO.setup(dt_pin, GPIO.IN, GPIO.PUD_UP)
  GPIO.setup(sw_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

  GPIO.add_event_detect(clk_pin, GPIO.FALLING, callback=rotation_decode, bouncetime=200)

def rotation_decode(pin):
    global counter
    global clkLastState
    clockState = GPIO.input(27)
    if clockState != clkLastState:
        if GPIO.input(dt_pin) == 0:
            counter -= 1
            if counter < 0:
                counter = 0
            print('Rolling to the LEFT')
            print(counter)
        else:
            counter += 1
            if counter > 10:
                counter = 10
            print("Rolling to the RIGHT")
            print(counter)
        clockState=clkLastState 

setup()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt as e:
    print(e)
finally:
    print("Program stopped...")

