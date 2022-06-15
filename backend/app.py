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
mode_counter = 0

#######     temp lezen code    #######

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
if mode_counter == 0:
        try:
            def read_temp():
                    global temp
                    file = open('/sys/bus/w1/devices/28-0620198ec89f/w1_slave')
                    text = file.read()
                    file.close()
                    secondline = text.split("\n")[1]
                    temperatuurdata = secondline.split(" ")[9]
                    temperatuur = float(temperatuurdata[2:])
                    temp = round(temperatuur / 1000, 2)
                    answer=DataRepository.insert_temp(temp)      
                    SocketIO.emit('B2F_refresh', {'data': temp}, broadcast=True)
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

        except KeyboardInterrupt as KI:
            print(KI)


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

if mode_counter == 1:
        try:
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


#######     powerbtn code    #######

btnPin = Button(22)

def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    btnPin.on_press(lees_knop)

def lees_knop(pin):
    print("**** button pressed ****")
    #print(sudo shutdown now)

setup_gpio()
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt as e:
    print(e)
finally:
    print("Program stopped...")


#######     modebtn code    #######

btnPin = Button(27)

def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    btnPin.on_press(lees_knop)

def lees_knop(pin):
    print("**** button pressed ****")

setup_gpio()
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt as e:
    print(e)
finally:
    print("Program stopped...")




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