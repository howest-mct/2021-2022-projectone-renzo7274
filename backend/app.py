import sys
import time
from RPi import GPIO
from helpers.klasseknop import Button
import threading

from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify
from repositories.DataRepository import DataRepository

from selenium import webdriver

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options


GPIO.setmode(GPIO.BCM)


trans = 20
GPIO.setup(trans, GPIO.OUT)
pwm_trans = GPIO.PWM(trans, 50)
pwm_trans.start(0)

temp = {}

# ledPin = 21
# btnPin = Button(20)

# Code voor Hardware
    #temp sensor

try:
    while True:
        file = open('/sys/bus/w1/devices/28-22d540000900/w1_slave')
        text = file.read()
        file.close()
        secondline = text.split("\n")[1]
        temperatuurdata = secondline.split(" ")[9]
        temperatuur = float(temperatuurdata[2:])
        temp = round(temperatuur / 1000, 2)
        print("De temp is: =", temp, "graden Celcius.")
        huidige_temp()

except KeyboardInterrupt:
    pwm_trans.stop()
finally:
    GPIO.cleanup()

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




# Code voor Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False,
                    engineio_logger=False, ping_timeout=1)

CORS(app)


@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)



# API ENDPOINTS


@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."


@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    # # Send to the client!
    # vraag de status op van de lampen uit de DB
    status = DataRepository.read_status_lampen()
    emit('B2F_status_lampen', {'lampen': status}, broadcast=True)


# @socketio.on('F2B_switch_light')
# def switch_light(data):
#     # Ophalen van de data
#     lamp_id = data['lamp_id']
#     new_status = data['new_status']
#     print(f"Lamp {lamp_id} wordt geswitcht naar {new_status}")

    # # Stel de status in op de DB
    # res = DataRepository.update_status_lamp(lamp_id, new_status)

    # # Vraag de (nieuwe) status op van de lamp en stuur deze naar de frontend.
    # data = DataRepository.read_status_lamp_by_id(lamp_id)
    # socketio.emit('B2F_verandering_lamp', {'lamp': data}, broadcast=True)

    # # Indien het om de lamp van de TV kamer gaat, dan moeten we ook de hardware aansturen.
    # if lamp_id == '3':
    #     print(f"TV kamer moet switchen naar {new_status} !")
    #     GPIO.output(ledPin, new_status)



# START een thread op. Belangrijk!!! Debugging moet UIT staan op start van de server, anders start de thread dubbel op
# werk enkel met de packages gevent en gevent-websocket.

def start_thread():
    print("**** Starting THREAD ****")
    thread = threading.Thread(target=all_out, args=(), daemon=True)
    thread.start()


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



# ANDERE FUNCTIES


if __name__ == '__main__':
    try:
        #setup_gpio()
        start_thread()
        start_chrome_thread()
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0')
    except KeyboardInterrupt:
        print ('KeyboardInterrupt exception is caught')
    finally:
        GPIO.cleanup()

