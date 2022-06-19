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

from grove.adc import ADC
 
 
class GroveLoudnessSensor:
 
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC(address=8)
 
    @property
    def value(self):
        return self.adc.read(self.channel)
 
Grove = GroveLoudnessSensor

def main():
 
    sensor = GroveLoudnessSensor(0)
 
    print('Detecting loud...')
    while True:
        value = sensor.value
        if value > 10:
            print("Loud value {}, Loud Detected.".format(value))
            time.sleep(1)
 

if __name__ == '__main__':
    main()