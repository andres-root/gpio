from flask import Flask, render_template
from flask_socketio import SocketIO
import time
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


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
    data = {'author': 'serial_input', 'message': 'Hello from serial'}
    time.sleep(10)
    print('sleeped')
    socketio.emit('serial', data, callback=serial_read)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)
