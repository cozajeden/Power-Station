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
    while True:
        data = queue.get()
        ser.write(data.encode('utf-8'))
        if not data == 'GET_STATUS':
            socketio.emit('sending', data)
        queue.task_done()

def serial_listener():
    while True:
        data = ser.readline()
        print('recieved: ', data)
        data = data.decode('utf-8')
        if not data.startswith('1:'):
            socketio.emit('recieving', data.strip())
        else:
            handle_status_response(data.strip())

def handle_status_response(data: str):
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
    while True:
        queue.put('GET_STATUS')
        sleep(2)

@app.route('/')
async def index():
    return render_template('index.html')

@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))

@socketio.on('command')
def handle_json(command):
    command_queue.put(command)

if __name__ == '__main__':
    # def test():
    #     while True:
    #         data = {    1: 10,  2: 20,  3: 1233,  4: 40,  5: 50,  6: 630,  7: 70,  8: 80,  9: 90, 10: 100.34, 11: 54}
    #         data = {VALUE_MAPPING[key]: value for key, value in data.items()}
    #         socketio.emit('status', json.dumps(data))
    #         sleep(1)
    # test_thread = Thread(target=test, daemon=True)
    # test_thread.start()
    serial_thread = Thread(target=serial_handler, args=(command_queue,), daemon=True)
    listener_thread = Thread(target=serial_listener, daemon=True)
    cyclic_thread = Thread(target=cyclic_get_status, args=(command_queue,), daemon=True)
    serial_thread.start()
    listener_thread.start()
    cyclic_thread.start()
    socketio.run(app, host='0.0.0.0', port=5000)