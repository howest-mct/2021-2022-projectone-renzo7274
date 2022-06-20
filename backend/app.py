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
from subprocess import check_output
from selenium import webdriver

from grove.adc import ADC
from helpers.klassesound import GroveLoudnessSensor

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

GPIO.setmode(GPIO.BCM)
global mode_counter
mode_counter = 1

#######     fan control code    #######

trans = 6
def setup_trans():
    GPIO.setmode(GPIO.BCM)
    global pwm_trans
    GPIO.setup(trans, GPIO.OUT)
    pwm_trans = GPIO.PWM(trans, 50)
    pwm_trans.start(0)

clk_pin = 18
dt_pin = 17
sw_pin = 27
clkLastState = 0
switchState = 0
global fanspeed 
fanspeed = 0

def setup_encoder():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(clk_pin, GPIO.IN, GPIO.PUD_UP)
  GPIO.setup(dt_pin, GPIO.IN, GPIO.PUD_UP)
  GPIO.setup(sw_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

  GPIO.add_event_detect(clk_pin, GPIO.BOTH, callback=manual_fan, bouncetime=200)

def manual_fan(clk_pin):
    if mode_counter == 1:
        global fanspeed
        global clkLastState
        clockState = GPIO.input(18)
        if clockState != clkLastState:
            if GPIO.input(dt_pin) == 0:
                fanspeed-= 1
                if fanspeed < 0:
                    fanspeed = 0
                answer=DataRepository.insert_fanspeed(fanspeed)
            else:
                fanspeed+= 1
                if fanspeed > 10:
                    fanspeed = 10
                answer=DataRepository.insert_fanspeed(fanspeed)
            clockState=clkLastState
            update_fanspeed()

def update_fanspeed():
    global fanspeed
    print(f"fanspeed: {fanspeed}")
    if fanspeed == 1:
        pwm_trans.ChangeDutyCycle(20)                

    elif fanspeed == 2:
        pwm_trans.ChangeDutyCycle(30)                

    elif fanspeed == 3:
        pwm_trans.ChangeDutyCycle(40)                

    elif fanspeed == 4:
        pwm_trans.ChangeDutyCycle(50)                

    elif fanspeed == 5:
        pwm_trans.ChangeDutyCycle(60)               

    elif fanspeed == 6:
        pwm_trans.ChangeDutyCycle(70)                

    elif fanspeed == 7:
        pwm_trans.ChangeDutyCycle(80)               

    elif fanspeed == 8:
        pwm_trans.ChangeDutyCycle(90)               

    elif fanspeed == 9:
        pwm_trans.ChangeDutyCycle(95)                

    elif fanspeed == 10:
        pwm_trans.ChangeDutyCycle(100)                
    else:
        pwm_trans.ChangeDutyCycle(0)
                           


def auto_fan():
    global fanspeed
    temp = {}
    temp_0 = 20
    temp_1 = 25
    temp_2 = 30
    temp_3 = 35
    temp_4 = 40
    temp_5 = 45
    temp_6 = 50
    temp_7 = 55
    temp_8 = 60
    temp_9 = 65
    temp_10 = 70
    while True:
        stat = 0
        file = open('/sys/bus/w1/devices/28-0620198ec89f/w1_slave')
        text = file.read()
        file.close()
        secondline = text.split("\n")[1]
        temperatuurdata = secondline.split(" ")[9]
        temperatuur = float(temperatuurdata[2:])
        temp = round(temperatuur / 1000, 2)
        answer=DataRepository.insert_temp(temp)      
        print(f"{temp} °C")

        if mode_counter == 0:
            if temp >= temp_0 and temp < temp_1:
                pwm_trans.ChangeDutyCycle(20)
                if stat == 0:
                    fanspeed = 1
                    answer=DataRepository.insert_fanspeed(fanspeed)
                    stat = 1

            elif temp >= temp_1 and temp < temp_2:
                pwm_trans.ChangeDutyCycle(30)
                if stat == 0:
                    fanspeed = 2
                    answer=DataRepository.insert_fanspeed(fanspeed)
                    stat = 1

            elif temp >= temp_2 and temp < temp_3:
                pwm_trans.ChangeDutyCycle(40)
                if stat == 0:
                    fanspeed = 3
                    answer=DataRepository.insert_fanspeed(fanspeed)
                    stat = 1

            elif temp >= temp_3 and temp < temp_4:
                pwm_trans.ChangeDutyCycle(50)
                if stat == 0:
                    fanspeed = 4
                    answer=DataRepository.insert_fanspeed(fanspeed)
                    stat = 1

            elif temp >= temp_4 and temp < temp_5:
                pwm_trans.ChangeDutyCycle(60)
                if stat == 0:
                    fanspeed = 5
                    answer=DataRepository.insert_fanspeed(fanspeed)
                    stat = 1

            elif temp >= temp_5 and temp < temp_6:
                pwm_trans.ChangeDutyCycle(70)
                if stat == 0:
                    fanspeed = 6
                    answer=DataRepository.insert_fanspeed(fanspeed)
                    stat = 1

            elif temp >= temp_6 and temp < temp_7:
                pwm_trans.ChangeDutyCycle(80)
                if stat == 0:
                    fanspeed = 7
                    answer=DataRepository.insert_fanspeed(fanspeed)
                    stat = 1

            elif temp >= temp_7 and temp < temp_8:
                pwm_trans.ChangeDutyCycle(90)
                if stat == 0:
                    fanspeed = 8
                    answer=DataRepository.insert_fanspeed(fanspeed)
                    stat = 1

            elif temp >= temp_8 and temp < temp_9:
                pwm_trans.ChangeDutyCycle(95)
                if stat == 0:
                    fanspeed = 9
                    answer=DataRepository.insert_fanspeed(fanspeed)
                    stat = 1

            elif temp >= temp_10:
                pwm_trans.ChangeDutyCycle(100)
                if stat == 0:
                    fanspeed = 10
                    answer=DataRepository.insert_fanspeed(fanspeed)
                    stat = 1
            else:
                pwm_trans.ChangeDutyCycle(0)
                if stat == 0:
                    fanspeed = 0
                    answer=DataRepository.insert_fanspeed(fanspeed)
                    stat = 1

        time.sleep(2)


#######     lcd code    #######

e_pin = 20
rs_pin = 21


# lijst_pinnen
lijst_pinnen = [16, 12, 25, 24, 23, 26, 19, 13]

def setup_lcd():
    GPIO.setmode(GPIO.BCM)
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

def write_lcd():
    time.sleep(10)
    ips = check_output(['hostname', '--all-ip-addresses'])
    ips = ips.decode('utf-8')
    ips = ips.split()
    ip = ips[1]
    #print(f"IP: {ip}")
    write_message(f"IP: {ip}")
    time.sleep(2)


#######     sound sensor code    #######

def __init__(self, channel):
        self.channel = channel
        self.adc = ADC(address=8)
 
@property
def value(self):
    return self.adc.read(self.channel)
 
Grove = GroveLoudnessSensor

def sound_detect():
    sensor = GroveLoudnessSensor(0)
    sound = {}

    while True:
        value = sensor.value
        if value > 10:
            sound = value
            print(f"{sound} dB")
            answer=DataRepository.insert_sound(sound)
            time.sleep(3)


#######     powerbtn code    #######

pbtnPin = Button(22)

def setup_gpio_pbtn():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    pbtnPin.on_press(lees_knop_power)

def lees_knop_power(ppin):
    print("**** power button pressed ****")
    answer=DataRepository.insert_pbtn(1)
    # os.system("sudo poweroff")

setup_gpio_pbtn()


#######     modebtn code    #######

mbtnPin = Button(27)

def setup_gpio_mbtn():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    mbtnPin.on_press(lees_knop_mode)

 

def lees_knop_mode(mpin):
    global mode_counter
    if mode_counter == 1:
        mode_counter = 0
        print(mode_counter)
        print("**** button pressed: rotary ****")
        answer=DataRepository.insert_mbtn(mode_counter)
    else:
        mode_counter = 1
        print(mode_counter)
        print("**** button pressed: rotary ****")
        answer=DataRepository.insert_mbtn(mode_counter)

setup_gpio_mbtn()




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

@socketio.on('connect')
def initial_connection():
    print('A new client connect')

@socketio.on('B2F_refresh')
def data_status():
        status_celcius = DataRepository.read_latest_temp_data()
        status_decibel = DataRepository.read_latest_sound_data()
        socketio.emit('B2F_refresh', {'dataCelcius': status_celcius["waarde"], 'dataDecibel': status_decibel["waarde"]}, broadcast=True)
        print(f"data: {status_celcius, status_decibel}")

@socketio.on('F2B_switch_fanmode')
def switch_fanmode(data):
    global mode_counter
    print(f"{data}")
    if data == True:
        mode_counter = 0
    elif data == False:
        mode_counter = 1
    print(f"{mode_counter}")

@socketio.on('F2B_switch_fanspeed')
def switch_fanspeed(data):
    print(f"{data}")
    global fanspeed 
    fanspeed = int(data)
    update_fanspeed()




#######     threads    #######

# START een thread op. Belangrijk!!! Debugging moet UIT staan op start van de server, anders start de thread dubbel op
# werk enkel met de packages gevent en gevent-websocket.

def start_thread_afans():
    print("**** Calling THREAD afans ****")
    thread1 = threading.Thread(target=auto_fan, args=(), daemon=True)
    thread1.start()
    time.sleep(1)

def start_thread_mfans():
    print("**** Calling THREAD mfans ****")
    thread1 = threading.Thread(target=manual_fan, args=(), daemon=True)
    thread1.start()
    time.sleep(1)

def start_thread_sound():
    print("**** Calling THREAD sound ****")
    thread2 = threading.Thread(target=sound_detect, args=(), daemon=True)
    thread2.start()
    time.sleep(1.5)

def start_thread_pbtn():
    print("**** Calling THREAD pbtn ****")
    thread3 = threading.Thread(target=lees_knop_power, args=(), daemon=True)
    thread3.start()
    time.sleep(0.2)

def start_thread_mbtn():
    print("**** Calling THREAD mbtn ****")
    thread4 = threading.Thread(target=lees_knop_mode, args=(), daemon=True)
    thread4.start()
    time.sleep(0.3)


def start_threads():
    print("**** Starting THREADS ****")
    start_thread_afans()
    start_thread_mfans()
    start_thread_sound()
    start_thread_pbtn()
    start_thread_mbtn()




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
        setup_lcd()
        init_LCD()
        write_lcd()
        setup_trans()
        setup_encoder()
        start_threads()
        start_chrome_thread()   
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0')  
        # port=5000,
        while True: 
            time.sleep(1)
    except KeyboardInterrupt:
        print ('KeyboardInterrupt exception is caught')
    finally:
        GPIO.cleanup()