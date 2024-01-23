import time
from threading import Thread
import socketio_camera

camera_id = 1 #change this id for each camera
socket_server = "ws://localhost:12000" #change the server address

Socketio = Thread(target = socketio_camera.connect_server,args=[camera_id,socket_server])

Socketio.start()

#=============== AI Code Below ==============

#for example, update rack state every x second.
#state list index 0 is the bottom layer
#socketio_camera.update_rack() only update 1 rack per call

i=0

while True:
    i+=1
    if i>999:
        i=0

    time.sleep(2)
    socketio_camera.update_rack(1,[['red_state','green_state'],['yellow_state','green_state'],['green_state','green_state'],['yellow_state','red_state']])
    print('rack state changed: counter ', i)
    time.sleep(2)
    socketio_camera.update_rack(2,[['green_state','green_state'],['red_state','green_state'],['yellow_state','red_state'],['empty','empty']])

    time.sleep(2)
    socketio_camera.update_rack(1,[['yellow_state','red_state'],['yellow_state','red_state'],['yellow_state','green_state'],['red_state','green_state']])
    print('rack state changed: counter ', i)
    time.sleep(2)
    socketio_camera.update_rack(2,[['red_state','green_state'],['red_state','green_state'],['yellow_state','green_state'],['empty','empty']])








