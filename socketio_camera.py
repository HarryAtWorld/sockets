# pip install "python-socketio[client]"

import socketio

device_type = "camera"
device_id = 999
socket_sever = ""
sio = socketio.Client()

#===================export functions=============================

def connect_server(camera_id,server_ip):
    try_connect(camera_id,server_ip)

def try_connect(camera_id,server_ip):

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
            print(f"\n == Got Error on Connection Initialize ==\n{error}\nWill retry after 3s.")
        sio.sleep(3)   

    sio.wait()

def yellow_alarm():
    while True:        
        try:
            sio.emit('yellow_alarm',{})
            break
        except:
            print('re-trying, yellow alarm')
            sio.sleep(1)


def red_alarm():
    while True:        
        try:
            sio.emit('red_alarm',{})
            break
        except:
            print('re-trying, red alarm')
            sio.sleep(1)

#=====================Socket IO Events===========================

@sio.event
def connect():
    print('== Server Connected ==')
    sio.emit("register",{"device_type":device_type,"device_id":device_id})
    
@sio.event
def disconnect():
    print('== Server Disconnected ==')


if __name__ == '__main__':
    connect_server(47,"ws://localhost:12000")






