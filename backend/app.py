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

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options


GPIO.setmode(GPIO.BCM)


#######     temp lezen code    #######

trans = 20
GPIO.setup(trans, GPIO.OUT)
pwm_trans = GPIO.PWM(trans, 50)
pwm_trans.start(0)

temp = {}

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
        tekst = ("192.168.168.169")
        write_message(tekst)
        time.sleep(10)
except KeyboardInterrupt as KI:
    print(KI)
finally:
    GPIO.cleanup()
    print('Program stopped...')


#######     rotary encoder code    #######

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
        time.sleep(0.1)
except KeyboardInterrupt as e:
    print(e)
finally:
    print("Program stopped...")


#######     btn code    #######

# ledPin = 21
# btnPin = Button(20)

# Code voor Hardware
    #temp sensor

# def setup_gpio():
#     GPIO.setwarnings(False)
#     GPIO.setmode(GPIO.BCM)

#     GPIO.setup(ledPin, GPIO.OUT)
#     GPIO.output(ledPin, GPIO.LOW)
    
#     btnPin.on_press(lees_knop)

# def lees_knop(pin):
#     if btnPin.pressed:
#         print("**** button pressed ****")
#         if GPIO.input(ledPin) == 1:
#             switch_light({'lamp_id': '3', 'new_status': 0})
#         else:
#             switch_light({'lamp_id': '3', 'new_status': 1})




#######     Flask code    #######

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False,
                    engineio_logger=False, ping_timeout=1)

CORS(app)

@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)




#######     API ENDPOINTS    #######
endpoint = "/api/v1"

@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

@app.route(endpoint + '/temp', methods=['GET'])
def get_temp():
    if request.method == 'GET':
        data = DataRepository.read_latest_temp_data()
        if data is not None:
            return jsonify(data=data), 200
        else:
            return jsonify(data="ERROR"), 404

@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    # # Send to the client!
    # vraag de status op van de lampen uit de DB




#######     threads    #######

# START een thread op. Belangrijk!!! Debugging moet UIT staan op start van de server, anders start de thread dubbel op
# werk enkel met de packages gevent en gevent-websocket.

def start_thread():
    print("**** Starting THREAD ****")
    thread = threading.Thread(target=read_temp, args=(), daemon=True)
    thread.start()
    time.sleep(5)

def start_thread():
    print("**** Starting THREAD ****")
    thread = threading.Thread(target=write_message, args=(), daemon=True)
    thread.start()
    time.sleep(10)

def start_thread():
    print("**** Starting THREAD ****")
    thread = threading.Thread(target=rotation_decode, args=(), daemon=True)
    thread.start()
    time.sleep(0.5)




#######     chrome kiosk    #######

def start_chrome_kiosk():
    import os

    os.environ['DISPLAY'] = ':0.0'
    options = webdriver.ChromeOptions()
    # options.headless = True
    # options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    # options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    # options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--kiosk')
    # chrome_options.add_argument('--no-sandbox')         
    # options.add_argument("disable-infobars")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    driver.get("http://localhost")
    while True:
        pass

def start_chrome_thread():
    print("**** Starting CHROME ****")
    chromeThread = threading.Thread(target=start_chrome_kiosk, args=(), daemon=True)
    chromeThread.start()




#######     ANDERE FUNCTIES    #######

if __name__ == '__main__':
    try:
        # setup_gpio()
        start_chrome_thread()   
        start_thread()
        print("**** Starting APP ****")
        socketio.run(app, port=5000, debug=False, host='0.0.0.0')   
    except KeyboardInterrupt:
        print ('KeyboardInterrupt exception is caught')
    finally:
        GPIO.cleanup()