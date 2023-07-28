from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from threading import Thread
from queue import Queue
import serial
from time import sleep

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='threading')

command_queue = Queue()
ser = serial.Serial('COM5', 115200)

def serial_handler(queue: Queue):
    while True:
        data = queue.get()
        ser.write(data.encode('utf-8'))
        socketio.emit('sending', data)
        queue.task_done()

def serial_listener():
    while True:
        data = ser.read(1024)
        data = data.decode('utf-8')
        print('recieved: ', data)
        socketio.emit('recieving', data)

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
    serial_thread = Thread(target=serial_handler, args=(command_queue,), daemon=True)
    listener_thread = Thread(target=serial_listener, daemon=True)
    cyclic_thread = Thread(target=cyclic_get_status, args=(command_queue,), daemon=True)
    serial_thread.start()
    listener_thread.start()
    cyclic_thread.start()
    socketio.run(app, host='0.0.0.0', port=5000)