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

btnPin = Button(27)

def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    btnPin.on_press(lees_knop)

def lees_knop(pin):
    print("**** button pressed ****")
setup_gpio()
while True:
    time.sleep(0)