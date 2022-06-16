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

#######     lcd code    #######

e_pin = 20
rs_pin = 21

GPIO.setmode(GPIO.BCM)

# lijst_pinnen
lijst_pinnen = [16, 12, 25, 24, 23, 26, 19, 13]

def setup():
    GPIO.setup(e_pin, GPIO.OUT)
    GPIO.setup(rs_pin, GPIO.OUT)
    for i in range(8):
        GPIO.setup(lijst_pinnen[i], GPIO.OUT)
    GPIO.output(e_pin, GPIO.HIGH)

# RS laag, set_data_bits, E laag, E hoog
def send_instruction(value):
    GPIO.output(rs_pin, GPIO.LOW)
    set_data_bits(value)
    GPIO.output(e_pin, GPIO.LOW)
    GPIO.output(e_pin, GPIO.HIGH)
    time.sleep(0.01)

# RS hoog, set_data_bits, E laag, E hoog
def send_character(value):
    value = ord(value)
    GPIO.output(rs_pin, GPIO.HIGH)
    GPIO.output(e_pin, GPIO.HIGH)
    set_data_bits(value)
    GPIO.output(e_pin, GPIO.LOW)
    GPIO.output(e_pin, GPIO.HIGH)
    time.sleep(0.01)

# value = byte, loop trough bits (mask) and set data pins
def set_data_bits(value):
    check_value = 0b1
    for i in range(8):
        te_verzenden_value = value & check_value
        if te_verzenden_value > 0:
            GPIO.output(lijst_pinnen[i], GPIO.HIGH)
        else:
            GPIO.output(lijst_pinnen[i], GPIO.LOW)
        check_value = check_value << 1

# function set, display on, clear display en cursor home
def write_message(message):
    send_instruction(0b00000001)
    count = 0
    for i in message:
        count += 1
        send_character(i)
        if count == 16:
            send_instruction(0b10000000 | 0x40)

def init_LCD():
    send_instruction(0b00111000)  # function set of 0x38
    send_instruction(0b00001111)  # display on of 0xf
    send_instruction(0b00000001)  # clear display/cursor home of 0x01

setup()
init_LCD()
try:
    while True:
        tekst = ("ip")
        write_message(tekst)
        time.sleep(10)
except KeyboardInterrupt as KI:
    print(KI)
finally:
    GPIO.cleanup()
    print('Program stopped...')