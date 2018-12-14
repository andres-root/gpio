from flask import Flask, render_template
from flask_socketio import SocketIO
import time
import json
from gpiozero import LED


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
blue_led = LED(23)
red_led = LED(24)


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/blue/')
def blue():
    blue_led.on()
    time.sleep(1)
    blue_led.off()
    time.sleep(1)
    blue_led.on()
    time.sleep(1)
    blue_led.off()
    time.sleep(1)
    blue_led.on()
    time.sleep(1)
    blue_led.off()
    time.sleep(1)
    # return render_template('blue.html')


# @app.route('/red/')
def red():
    red_led.on()
    time.sleep(1)
    red_led.off()
    time.sleep(1)
    red_led.on()
    time.sleep(1)
    red_led.off()
    time.sleep(1)
    red_led.on()
    time.sleep(1)
    red_led.off()
    time.sleep(1)
    # return render_template('red.html')


def messageReceived(methods=['GET', 'POST']):
    print('Message received')


@socketio.on('hello')
def handle_event(json, methods=['GET', 'POST']):
    print('Received event: {0}'.format(json))
    socketio.emit('Hello', json, callback=messageReceived)


def serial_read(methods=['GET', 'POST']):
    print('Message received serial')


@socketio.on('connect2pi')
def handle_serial(json_data, methods=['GET', 'POST']):
    print('Connected from {0}'.format(json_data))
    data = {'message': 'Connected to serial'}
    socketio.emit('serial', json.dumps(data), callback=serial_read)


@socketio.on('led')
def handle_led(json_data, methods=['GET', 'POST']):
    print('Received event: {0}'.format(json))

    led = int(json_data['color'])

    if led == 23:
        blue()
    elif led == 24:
        red()
    else:
        print('Pin {0} is not being used'.format(led))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)
