from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'notverysecret!'
socketio = SocketIO(app)

@app.route("/")
def hello():
    return render_template('index.html')

@socketio.on("client_to_server")
def client_to_server(msg):
    message = "pong"
    print("message from server to client: " + message)
    socketio.emit("server_to_client", {"msg": message})

if __name__ == '__main__':
    socketio.run(app,port=8000, host='0.0.0.0', debug=True)
    print('socket io start')