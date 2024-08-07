# pip install "python-socketio[client]"

import socketio

device_type = "edge_computer"
device_id = 999
socket_sever = ""
cameras=[]
sio = socketio.Client()

#===================export functions=============================

def connect_server(computer_id,camera_list,server_ip):

    global device_id
    global socket_sever
    global cameras
    device_id=computer_id
    cameras = camera_list
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

def closeConnection():
    sio.disconnect()

def yellow_alarm(camera_id):
    if not camera_id in cameras:
        print('<<<<< Input ID not existed >>>>>')
        return

    while True:        
        try:
            sio.emit('yellow_alarm',{"camera_id":camera_id})
            break
        except:
            print('re-trying, yellow alarm sending')
            sio.sleep(1)


def red_alarm(camera_id):
    if not camera_id in cameras:
        print('<<<<< Input ID not existed >>>>>')
        return
    while True:        
        try:
            sio.emit('red_alarm',{"camera_id":camera_id})
            break
        except:
            print('re-trying, red alarm sending')
            sio.sleep(1)


#Not ready for use
#for display the drowning location. left top is [0,0].
def alarm_location(camera_id,alarm,x,y):
    if not camera_id in cameras:
        print('<<<<< Input ID not existed >>>>>')
        return
    while True:        
        try:
            sio.emit('alarm_location',{"camera_id":camera_id,"alarm":[x,y,alarm]})
            break
        except:
            print('re-trying, alarm location sending')
            sio.sleep(1)

def cancel_alarm_location(camera_id,alarm,x,y):
    if not camera_id in cameras:
        print('<<<<< Input ID not existed >>>>>')
        return
    while True:        
        try:
            sio.emit('cancel_alarm_location',{"camera_id":camera_id,"alarm":[x,y,alarm]})
            break
        except:
            print('re-trying, cancel alarm sending')
            sio.sleep(1)


def cancel_alarm(camera_id):
    print('<<<<< Cancel >>>>>')
    if not camera_id in cameras:
        return
    while True:        
        try:
            sio.emit('cancel_alarm',{"camera_id":camera_id})
            break
        except:
            print('re-trying, cancel alarm sending')
            sio.sleep(1)

def camera_error(camera_id):
    if not camera_id in cameras:
        print('<<<<< Input ID not existed >>>>>')
        return
    while True:
        try:
            sio.emit('camera_error',{"camera_id":camera_id})
            break
        except:
            print('re-trying, camera error message sending')
            sio.sleep(1)

#for Camera been blocked.
def camera_blocked(camera_id):
    if not camera_id in cameras:
        print('<<<<< Input ID not existed >>>>>')
        return
    while True:        
        try:
            sio.emit('camera_blocked',{"camera_id":camera_id})
            break
        except:
            print('re-trying, camera blocked sending')
            sio.sleep(1)

def camera_resumed(camera_id):
    if not camera_id in cameras:
        print('<<<<< Input ID not existed >>>>>')
        return
    while True:
        try:
            sio.emit('camera_resumed',{"camera_id":camera_id})
            break
        except:
            print('re-trying, camera resumed message sending')
            sio.sleep(1)

#=====================Socket IO Events===========================

@sio.event
def connect():
    print('== Server Connected ==')
    sio.emit("register",{"device_type":device_type,"computer_id":device_id,"camera_list":cameras})
    
@sio.event
def disconnect():
    print('== Server Disconnected ==')


if __name__ == '__main__':
    connect_server(1,[5,6,7],"ws://localhost:12000")






