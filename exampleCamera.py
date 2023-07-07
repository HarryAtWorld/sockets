import time
from threading import Thread
import socketio_camera

camera_id = 7  #change this for each camera
socket_server = "ws://192.168.88.24:12000" #change the server address

Socket9 = Thread(target = socketio_camera.connect_server,args=[camera_id,socket_server])


Socket9.start()


#========== AI Code Below ==============

#for example, sent alarm to server every 4 second.
while True:
    time.sleep(5)
    print('trigger yellow alarm')

    socketio_camera.yellow_alarm()
    # socketio_camera.red_alarm()







