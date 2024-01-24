import time
from threading import Thread
import socketio_camera

camera_id = 1 #change this id for each camera
socket_server = "ws://localhost:12000" #change the server address

Socketio = Thread(target = socketio_camera.connect_server,args=[camera_id,socket_server])

Socketio.start()

#=============== AI Code Below ==============

#for example, update rack state every x second.


i=0

while True:
    i+=1
    if i>999:
        i=0

    socketio_camera.update_rack_raw([0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    time.sleep(1)
    socketio_camera.update_rack_raw([1,0,0,0,1,0,0,0,0,0,2,1,0,2])
    time.sleep(1)
    socketio_camera.update_rack_raw([1,0,1,0,1,0,0,1,0,1,2,2,1,1])
    time.sleep(1)