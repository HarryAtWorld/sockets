import time
from threading import Thread
import socketio_camera

computer_id = 1  #change this id for Computer
# camera_list = [1,3,5,6,7,8,9,10,12,28,33,37,41,42,43,45,47] #change this list for cameras' id monitored by this computer
camera_list = [1,2,3,4] 
socket_server = "ws://localhost:12000" #change the server address

Socketio = Thread(target = socketio_camera.connect_server,args=[computer_id,camera_list,socket_server])

Socketio.start()

#=============== AI Code Below ==============

#for example, sent alarm to server every x second.

i=0
# socketio_camera.red_alarm(28)

# for i in camera_list:
#     if i >28:
#         socketio_camera.yellow_alarm(i)
#         print('-')
#     else:
#         socketio_camera.yellow_alarm(i)
#         print('-')
#     time.sleep(0.5)

# socketio_camera.red_alarm(28)

while True:
    i+=1
    if i>999:
        i=0

    # for i in camera_list:
    #     if i >28:
    #         socketio_camera.yellow_alarm(i)
    #         print('-')
    #     else:
    #         socketio_camera.yellow_alarm(i)
    #         print('-')
    #     time.sleep(1)

    # c
    # time.sleep(1)
    # socketio_camera.camera_error(5)
    # time.sleep(1)
    # socketio_camera.camera_resumed(5)
    # time.sleep(1)


    # socketio_camera.alarm_location(1,"yellow_alarm",2250,385)
    # socketio_camera.alarm_location(1,"yellow_alarm",1250,385)
    # time.sleep(3)
    socketio_camera.alarm_location(2,"red_alarm",1250,385)
    time.sleep(5)
    # socketio_camera.alarm_location(2,"yellow_alarm",125,385)
    # time.sleep(0.5)
    # socketio_camera.alarm_location(1,"yellow_alarm",2500,385)
    # time.sleep(3)
    # socketio_camera.alarm_location(1,"yellow_alarm",1250,385)
    # time.sleep(3)
    # socketio_camera.alarm_location(3,"red_alarm",300,200)
    # time.sleep(3)
    # socketio_camera.cancel_alarm_location(3,"red_alarm",300,200)
    # socketio_camera.cancel_alarm_location(1,"yellow_alarm",1250,385)
    # time.sleep(3)
    socketio_camera.cancel_alarm_location(2,"red_alarm",1250,385)
    time.sleep(5)
    # socketio_camera.cancel_alarm_location(2,"yellow_alarm",125,385)
    # time.sleep(3)

    # socketio_camera.cancel_alarm_location(1,"yellow_alarm",10,30)
    # time.sleep(3)

    # socketio_camera.yellow_alarm(5)
    # time.sleep(3)
    # socketio_camera.cancel_alarm(5)
    # time.sleep(3)
    

    # socketio_camera.camera_blocked(6)
    # time.sleep(3)
    # socketio_camera.camera_resumed(6)
    # time.sleep(3)

    # socketio_camera.camera_error(5)
    # time.sleep(3)
    # socketio_camera.camera_resumed(5)
    # time.sleep(3)

    

#     socketio_camera.yellow_alarm(1)
#     print('trigger yellow alarm: counter ', i)
#     time.sleep(3)
#     socketio_camera.red_alarm(3)
#     print('trigger red alarm: counter ', i)
#     time.sleep(3)
# #     socketio_camera.camera_error(8)
# #     print('trigger camera error: counter ', i)
# #     time.sleep(5)
# #     socketio_camera.camera_error(7)
# #     print('trigger red alarm: counter ', i)
# #     time.sleep(5)








