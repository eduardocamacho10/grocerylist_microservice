import os
import time
import zmq

# Directory to store recipe files
RECIPE_DIRECTORY = "recipes"
os.makedirs(RECIPE_DIRECTORY, exist_ok=True)

# File paths for communication
REQUEST_FILE = "request.txt"
RESPONSE_FILE = "response.txt"

# ZeroMQ 
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

def save_recipe(name, ingredients):
    """Save the recipe to a txt file."""
    file_path = os.path.join(RECIPE_DIRECTORY, f"{name}.txt")
    with open(file_path, "w") as f:
        f.write("\n".join(ingredients))
    return f"Recipe '{name}' saved successfully."

def list_recipes():
    """List stored recipes."""
    return "\n".join(os.listdir(RECIPE_DIRECTORY))

def get_recipe(name):
    """Retrieve a recipe by name."""
    file_path = os.path.join(RECIPE_DIRECTORY, f"{name}.txt")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    return f"Recipe '{name}' not found."

while True:
    # Check if request file exists
    if os.path.exists(REQUEST_FILE):
        with open(REQUEST_FILE, "r") as f:
            lines = f.readlines()
        
        if lines:
            command = lines[0].strip()
            name = lines[1].strip() if len(lines) > 1 else ""
            ingredients = lines[2:] if len(lines) > 2 else []
            
            if command == "save":
                response = save_recipe(name, ingredients)
            elif command == "get":
                response = get_recipe(name)
                
                # Write response to file
                with open(RESPONSE_FILE, "w") as f:
                    f.write(response)
                os.remove(REQUEST_FILE)
    
    # Check for ZeroMQ requests
    try:
        if socket.poll(100): 
            message = socket.recv_json()
            command = message.get("command")
            name = message.get("name")
            
            if command == "list":
                response = list_recipes()
            elif command == "get":
                response = get_recipe(name)
            else:
                response = "Invalid command."
            
            socket.send_json(response)
    except Exception as e:
        pass  
    
    time.sleep(1)  
