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