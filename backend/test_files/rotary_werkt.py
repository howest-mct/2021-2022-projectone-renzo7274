import sys
import time
from RPi import GPIO
from helpers.klasseknop import Button
import threading
import os
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify, request
from repositories.DataRepository import DataRepository
from selenium import webdriver

GPIO.setmode(GPIO.BCM)
mode_counter = 1

#######     rotary encoder code    #######

trans = 6

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
  

if mode_counter == 1:
        try:
            GPIO.setup(trans, GPIO.OUT)
            pwm_trans = GPIO.PWM(trans, 50)
            pwm_trans.start(0)
            def rotation_decode(clk_pin):
                global counter
                global clkLastState
                clockState = GPIO.input(18)
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

                if counter == 1:
                    pwm_trans.ChangeDutyCycle(20)

                elif counter == 2:
                    pwm_trans.ChangeDutyCycle(30)

                elif counter == 3:
                    pwm_trans.ChangeDutyCycle(40)

                elif counter == 4:
                    pwm_trans.ChangeDutyCycle(50)

                elif counter == 5:
                    pwm_trans.ChangeDutyCycle(60)

                elif counter == 6:
                    pwm_trans.ChangeDutyCycle(70)

                elif counter == 7:
                    pwm_trans.ChangeDutyCycle(80)

                elif counter == 8:
                    pwm_trans.ChangeDutyCycle(90)

                elif counter == 9:
                    pwm_trans.ChangeDutyCycle(95)

                elif counter == 10:
                    pwm_trans.ChangeDutyCycle(100)
                else:
                    pwm_trans.ChangeDutyCycle(0)
        
        except KeyboardInterrupt as e:
            print(e)
setup()
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt as e:
    print(e)
finally:
    print("Program stopped...")