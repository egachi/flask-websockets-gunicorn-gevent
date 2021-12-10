from flask import Flask, render_template, session, copy_current_request_context
from flask_socketio import SocketIO, emit, disconnect
from threading import Lock
import os
async_mode = None
app = Flask(__name__)
 
socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins="*")
thread = None
thread_lock = Lock()
 
@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)
 
@socketio.on('my_event', namespace='/test')
def test_message(message):
    print('receive message:' + message['data'],)
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})
 
@socketio.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    print('broadcast message:' + message['data'],)
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)
 
@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()
 
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)
 
if __name__ == '__main__':
    socketio.run(app,port=5000, host='0.0.0.0', debug=True)
    print('socket io start')