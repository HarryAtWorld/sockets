# pip install "python-socketio[client]"

import socketio
import time

device_type = "camera"
device_id = 999
socket_sever = ""
sio = socketio.Client()

#===================export functions=============================
def connect_server(camera_id,server_ip):

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
            print(error,"\n\n ==Got Error on Connection Initialize==\nWill retry after 3s.")
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
def say_hi(data):
    print('say hi received')

@sio.event
def connect():
    print('==Server Connected==')
    sio.emit("register",{"device_type":device_type,"device_id":device_id})
    
@sio.event
def disconnect():
    print('==Server Disconnected==')



if __name__ == '__main__':
    connect_server(47,"ws://192.168.88.112:12000")





