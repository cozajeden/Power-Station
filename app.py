from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from threading import Thread
from queue import Queue
import serial
from time import sleep
import traceback
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='threading')

VALUE_MAPPING = {
    1: "Prąd lodówki",
    2: "Prąd zasilacza 2",
    3: "Prąd akumilatora",
    4: "Napięcie akumilatora",
    5: "Napięcie panelu słonecznego",
    6: "Napięcie zasilacza 1",
    7: "Prąd gniazda ładowania 1",
    8: "Prąd gniazda ładowania 2",
    9: "Temperatura ciepłej wody",
    10: "Temperatura wewnątrz lodówki",
    11: "Temperatura zimnej strony"
}

command_queue = Queue()
ser = serial.Serial('COM5', 115200)

def serial_handler(queue: Queue):
    """"This function is responsible for sending data to serial port"""
    while True:
        data = queue.get()
        ser.write(data.encode('utf-8'))
        if not data == 'GET_STATUS':
            socketio.emit('sending', data)
        queue.task_done()

def serial_listener():
    """"This function is responsible for listening to serial port"""
    while True:
        data = ser.readline()
        print('recieved: ', data)
        data = data.decode('utf-8')
        if not data.startswith('1:'):
            socketio.emit('recieving', data.strip())
        else:
            handle_status_response(data.strip())

def handle_status_response(data: str):
    """This function is responsible for parsing status response and sending it to client"""
    try:
        parsed_data = {
            VALUE_MAPPING[int(val.split(':')[0])]: int(val.split(':')[1])/100
            for val in data.split(',')
        }
        socketio.emit('status', json.dumps(parsed_data))
    except Exception as e:
        traceback.print_exc()
        print('error parsing status response: ', data)

def cyclic_get_status(queue: Queue):
    """This function is responsible for cyclically sending GET_STATUS command to serial port"""
    while True:
        queue.put('GET_STATUS')
        sleep(2)

@app.route('/')
async def index():
    """This function is responsible for rendering index.html"""
    return render_template('index.html')

@socketio.on('command')
def handle_json(command):
    """"This function is responsible for handling commands from client"""
    command_queue.put(command)

if __name__ == '__main__':
    serial_thread = Thread(target=serial_handler, args=(command_queue,), daemon=True)
    listener_thread = Thread(target=serial_listener, daemon=True)
    cyclic_thread = Thread(target=cyclic_get_status, args=(command_queue,), daemon=True)
    serial_thread.start()
    listener_thread.start()
    cyclic_thread.start()
    socketio.run(app, host='0.0.0.0', port=5000)