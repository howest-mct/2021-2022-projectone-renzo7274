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
mode_counter = 0

#######     powerbtn code    #######

btnPin = Button(22)

def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    btnPin.on_press(lees_knop_power)

def lees_knop_power(pin):
    print("**** button pressed ****")
    os.system("sudo poweroff")

setup_gpio()
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt as e:
    print(e)
finally:
    print("Program stopped...")