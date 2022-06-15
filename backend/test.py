import sys
import time
from RPi import GPIO
from helpers.klasseknop import Button
import threading
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify, request
from repositories.DataRepository import DataRepository
from selenium import webdriver

#######     powerbtn code    #######

import math
import sys
import time
from grove.adc import ADC
 
 
class GroveLoudnessSensor:
 
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()
 
    @property
    def value(self):
        return self.adc.read(self.channel)
 
Grove = GroveLoudnessSensor
 
 
def main():
    if len(sys.argv) < 2:
        print('Usage: {} adc_channel'.format(sys.argv[0]))
        sys.exit(1)
 
    sensor = GroveLoudnessSensor(int(sys.argv[1]))
 
    print('Detecting loud...')
    while True:
        value = sensor.value
        if value > 10:
            print("Loud value {}, Loud Detected.".format(value))
            time.sleep(.5)
 
if __name__ == '__main__':
    main()
