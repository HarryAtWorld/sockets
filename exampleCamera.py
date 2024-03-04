import time
from threading import Thread
import socketio_camera

computer_id = 1  #change this id for Computer
camera_list = [1,3,5,6,7,8,9,10] #change this list for cameras' id monitored by this computer
socket_server = "ws://localhost:12000" #change the server address

Socketio = Thread(target = socketio_camera.connect_server,args=[computer_id,camera_list,socket_server])

Socketio.start()

#=============== AI Code Below ==============

#for example, sent alarm to server every x second.

i=0

while True:
    i+=1
    if i>999:
        i=0

    socketio_camera.yellow_alarm(1)
    print('trigger yellow alarm: counter ', i)
    time.sleep(2)
    socketio_camera.red_alarm(1)
    print('trigger red alarm: counter ', i)
    time.sleep(2)
    socketio_camera.camera_error(1)
    print('trigger camera error: counter ', i)
    time.sleep(2)








