# grocerylist_microservice

REQUESTING DATA
----------------------------
The microservice provides a way to save and retrieve recipes using file-based communication (request.txt, response.txt) and ZeroMQ messaging.

format:
get
<Recipe_Name>

code Example:

with open("request.txt", "w") as f:
    f.write("save\nPizza\nDough\nTomato Sauce\nCheese\n")

RECEIVING DATA
-----------------
After request is sent, response will be written in response.txt

import time

# Wait for the response file to be created
time.sleep(2)
if os.path.exists("response.txt"):
    with open("response.txt", "r") as f:
        print("Recipe Retrieved:\n", f.read())

REQUESTING & RECEIVING DATA USING ZEROMQ
-----------------------------------------

SAVING RECIPE ZEROMQ
--------------------
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

save_request = {
    "command": "save",
    "name": "Burger",
    "ingredients": ["Bun", "Patty", "Lettuce", "Tomato", "Cheese", "Ketchup", "Mustard"]
}

print("Sending request to save 'Burger' recipe")
socket.send_json(save_request)
response = socket.recv_json()
print(f"Response: {response}")

Retrieving a Recipe (ZeroMQ)
----------------------------
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

get_request = {"command": "get", "name": "Burger"}

print("Requesting 'Burger' recipe...")
socket.send_json(get_request)
response = socket.recv_json()
print("Recipe Retrieved:\n", response)

UML SEQUENCE
-------------

![Screenshot 2025-03-11 at 10 35 42 PM](https://github.com/user-attachments/assets/db61c119-0297-42fc-b3ac-a9ee34366755)
![Screenshot 2025-03-11 at 10 35 51 PM](https://github.com/user-attachments/assets/ba3667f0-6207-4cf8-b87b-c50e3b768665)




