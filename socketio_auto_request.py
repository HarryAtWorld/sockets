# pip install "python-socketio[client]"

import socketio
import time

device_type = "auto_requesting_machine"
device_id = 998
socket_sever = ""
sio = socketio.Client()

connection = True

#===================export functions=============================
def start_auto_request(camera_id,server_ip):

    global device_id
    global socket_sever
    device_id=camera_id
    socket_sever = server_ip

    #in case of client start connection while server is not yet set up.
    while True:
        try:        
            sio.connect(socket_sever)
            break
        except BaseException as error:
            print(f"\n\n ==Got Error on Connection Initialize==\n{error}\nWill retry after 3s.")
        time.sleep(3)

    sio.wait()

#for testing
def hi():
    while True:        
        try:
            sio.emit('say_hi',{})
            break
        except:
            print('re-trying')
            time.sleep(0.5)

def yellow_alarm():
    while True:        
        try:
            sio.emit('yellow_alarm',{})
            break
        except:
            print('re-trying')
            time.sleep(2)

def red_alarm():
    while True:        
        try:
            sio.emit('red_alarm',{})
            break
        except:
            print('re-trying')
            time.sleep(0.5)


#=====================Socket IO Events===========================


@sio.event
def connect():
    global connection
    print('==Server Connected==')
    connection = True
    while connection:
        try:
            sio.emit("request_latest_data",{})
            # print("== auto requesting latest data ==")
            time.sleep(3)
        except:
            time.sleep(3)
            print("#### ==== auto requesting --- some error ==== ####")
            continue
    
@sio.event
def disconnect():
    global connection
    connection = False
    print('==Server Disconnected==',f"connection {connection}")




if __name__ == '__main__':
    start_auto_request(998,"ws://192.168.1.60:12000")





