# pip install "python-socketio[client]"

import socketio
import time

device_type = "panel"
device_id = 999
socket_sever = ""
sio = socketio.Client()

# yellow_alarm_action = None
# red_alarm_action = None
# disconnect_action = None

#===================export functions=============================
def connect_server(panel_id,server_ip):

    global device_id
    global socket_sever
    device_id=panel_id
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


def cancel_alarm(cameraID:int):
    while True:        
        try:
            sio.emit('cancel_alarm', {"camera_id": cameraID});
            break
        except:
            print('re-trying')
            time.sleep(0.5)


# def provide_action_for_yellow_alarm(input_action):
#     yellow_alarm_action = input_action

# def provide_action_for_red_alarm(input_action):
#     red_alarm_action = input_action

# def provide_action_for_disconnected(input_action):
#     disconnect_action = input_action


#=====================Socket IO Events===========================

@sio.event
def connect():
    print('== Server Connected ==')
    sio.emit("register",{"device_type":device_type,"device_id":device_id})
    
@sio.event
def latest_data(data):

    for item in data['camera']:
        
        if item['state'] == 'connected':
            print(item['id'],item['state'])
            #panel action here for camera connected

        if item['state'] == 'yellow_alarm':
            print(item['id'],item['state'])
            #panel action here for Yellow Alarm

        if item['state'] == 'red_alarm':
            print(item['id'],item['state'])
            #panel action here for Red Alarm
        
        if item['state'] == 'disconnected':
            print(item['id'],item['state'])
            #panel action here for camera disconnected

    print('== Got Latest Data ==')


@sio.event
def disconnect():

    #panel actions here

    print('==Server Disconnected==')



# @sio.event
# def yellow_alarm():

#     #panel actions here

#     print('==! Yellow Alarm !==')

# @sio.event
# def red_alarm():

#     #panel actions here

#     print('==!!! Red Alarm !!!==')


if __name__ == '__main__':
    connect_server(2,"ws://192.168.88.112:12000");
    
