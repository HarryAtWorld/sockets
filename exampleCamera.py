import time
from threading import Thread
import socketio_camera

camera_id = 38  #change this for each camera
socket_server = "ws://192.168.1.60:12000" #change the server address

Socket9 = Thread(target = socketio_camera.connect_server,args=[camera_id,socket_server])


Socket9.start()



#========== AI Code Below ==============

#for example, sent alarm to server every 4 second.

i =0

# socketio_camera.yellow_alarm()
# time.sleep(10)
# socketio_camera.red_alarm()
# time.sleep(15)

# socketio_camera.yellow_alarm()
# time.sleep(10)
# socketio_camera.red_alarm()
while True:
    i+=1
    print('trigger yellow alarm: counter ', i)

    socketio_camera.yellow_alarm()
    time.sleep(10)
    socketio_camera.red_alarm()
    time.sleep(15)







