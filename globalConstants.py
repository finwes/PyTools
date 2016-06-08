from config import Config

def init():
    global config
    global running
    global fleetControl
    global server
    global login
    global password

    config = Config()
    running = True
    fleetControl = None
    server = ""
    login = ""
    password = ""