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


trans = 6
GPIO.setup(trans, GPIO.OUT)
pwm_trans = GPIO.PWM(trans, 50)
pwm_trans.start(0)

temp = {}
temp_0 = 30
temp_1 = 35
temp_2 = 40
temp_3 = 45
temp_4 = 50
temp_5 = 55
temp_6 = 60
temp_7 = 65
temp_8 = 70
temp_9 = 75
temp_10 = 80

def read_temp():
    while True:
        global temp
        file = open('/sys/bus/w1/devices/28-0620198ec89f/w1_slave')
        text = file.read()
        file.close()
        secondline = text.split("\n")[1]
        temperatuurdata = secondline.split(" ")[9]
        temperatuur = float(temperatuurdata[2:])
        temp = round(temperatuur / 1000, 2)
        answer=DataRepository.insert_temp(temp)      
        socketio.emit('B2F_refresh', {'data': temp}, broadcast=True)
        print("De temp is: =", temp, "graden Celcius.")

        if temp >= temp_0 and temp < temp_1:
            pwm_trans.ChangeDutyCycle(10)

        elif temp >= temp_1 and temp < temp_2:
            pwm_trans.ChangeDutyCycle(20)

        elif temp >= temp_2 and temp < temp_3:
            pwm_trans.ChangeDutyCycle(30)

        elif temp >= temp_3 and temp < temp_4:
            pwm_trans.ChangeDutyCycle(40)

        elif temp >= temp_4 and temp < temp_5:
            pwm_trans.ChangeDutyCycle(50)

        elif temp >= temp_5 and temp < temp_6:
            pwm_trans.ChangeDutyCycle(60)

        elif temp >= temp_6 and temp < temp_7:
            pwm_trans.ChangeDutyCycle(70)

        elif temp >= temp_7 and temp < temp_8:
            pwm_trans.ChangeDutyCycle(80)

        elif temp >= temp_8 and temp < temp_9:
            pwm_trans.ChangeDutyCycle(90)

        elif temp >= temp_10:
            pwm_trans.ChangeDutyCycle(100)
        else:
            pwm_trans.ChangeDutyCycle(0)
