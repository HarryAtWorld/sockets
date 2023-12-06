Central socketIO Server for drowning detection mobile devices

# Start server

> pip install -r requirements.txt

then run `socket_server.py`  
suggest using venv to run the server.

Remind: to perform better efficiency, server side should using async mode, and using`await loop.run_in_executor()` to run other imported functions.

# Client side

functions in `socketio_camaera.py`.  
The use example, see `exampleCamera.py`, using `yellow_alarm()` and `red_alarm()` to info server.

Remind: to implement the socket functions with multithreading, the client side socket should NOT using async mode.

# GPIO

install package , should run below script on nano:
>$ sudo pip install Jetson.GPIO

GPIO functions in `gpio.py`, if needed, import to server for using.

