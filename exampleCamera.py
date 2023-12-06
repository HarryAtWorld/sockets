import time
from threading import Thread
import socketio_camera

camera_id = 38  #change this id for each camera
socket_server = "ws://0.0.0.0:12000" #change the server address

Socketio = Thread(target = socketio_camera.connect_server,args=[camera_id,socket_server])

Socketio.start()

#=============== AI Code Below ==============

#for example, sent alarm to server every x second.

i=0

while True:
    i+=1
    if i>999:
        i=0

    time.sleep(2)
    socketio_camera.yellow_alarm()
    print('trigger yellow alarm: counter ', i)
    time.sleep(2)
    socketio_camera.red_alarm()
    print('trigger red alarm: counter ', i)







