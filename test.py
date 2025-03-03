import os
import time
import zmq

REQUEST_FILE, RESPONSE_FILE = "request.txt", "response.txt"

def test_file():
    with open(REQUEST_FILE, "w") as f:
        f.write("save\nPizza\nDough\nTomato Sauce\nCheese\n")
    time.sleep(2)
    if os.path.exists(RESPONSE_FILE):
        print(open(RESPONSE_FILE).read())
        os.remove(RESPONSE_FILE)

def test_zmq():
    socket = zmq.Context().socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    for req in [{"command": "list"}, {"command": "get", "name": "Pizza"}]:
        socket.send_json(req)
        print(socket.recv_json())

test_file()
test_zmq()