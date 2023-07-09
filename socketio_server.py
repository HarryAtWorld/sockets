#pip install python-socketio
#pip install eventlet

import eventlet
import socketio
import time
import asyncio
import json
from datetime import datetime
import os


camera_list = {} #Data Example: {Ejh3gs6d8SHG8 : {id:1, state:'connected',type:'camera'}, JD2ij24IJ2dbi5 : {id:2, state:'yellow_alarm',type:'camera'}}
mobile_device_list = {} #Data Example: same as camera list

panel_connection = {}#Data Example: {"1":<websocket object>}
panel_list = {} #Data Example: {"1":{state:'connected',type:'panel'}}

if not os.path.exists("./log/"):
    os.makedirs("./log/")    

#============== Panel - WebSocket Set Up ===========================
def api_hook(input_api,panel_id):
    global panel_connection
    panel_connection[panel_id] = input_api


async def send(connection,message):
    try:
        await connection.send(message)
    except BaseException as e:
            print('sender error : ',e)


async def stp(message):
    global panel_connection

    connections = [send(panel_connection[connection],message) for connection in panel_connection]

    await asyncio.gather(*connections)
           

def send_to_panel(message):
    asyncio.run(stp(message))


#=============== SocketIO Setting ===================================


sio = socketio.Server(logger=False,engineio_logger=False,async_mode='eventlet')
app = socketio.WSGIApp(sio)


#================ When Device Connection Started ================
@sio.event
def connect(sid, environ):    
    print('\n========================')
    print('== Connection Created ==')
    print('========================')
    print('new device socket ID:',sid)

#================ Devices Register =======================
@sio.event
def register(sid, data):    
    if data["device_type"] == 'camera': 
        camera_list[sid] = {'id':data["device_id"],'state':'connected','type':data["device_type"]}
        sio.emit('latest_data',get_updated_list())
        save_log(f" camera {camera_list[sid]['id']}"," Connected")

        print('\n=======================')
        print("== Camera Registered ==")
        print('=======================')
        print("camera no.",data["device_id"],",",' internal socket ID:',sid)
        print_latest_list()

    elif data['device_type'] == 'mobile_device':
        
        mobile_device_list[sid] = {'id':data["device_id"],'state':'connected','type':data["device_type"]}
        sio.emit('latest_data',get_updated_list())
        save_log(f" mobile device {mobile_device_list[sid]['id']}"," Connected")

        print('\n==============================')
        print("== Mobile Device Registered ==")
        print('==============================')
        print("mobile device no.",data["device_id"],",",' internal socketID: ',sid)
        print_latest_list()

    # elif data['device_type'] == 'panel':
        
    #     panel_list[sid] = {'id':data["device_id"],'state':'connected','type':data["device_type"]}
    #     sio.emit('latest_data',get_updated_list())

    #     print('\n======================')
    #     print("== Panel Registered ==")
    #     print('======================')
    #     print("panel no.",data["device_id"],",",' internal socketID: ',sid)
    #     print_latest_list()

@sio.event
def request_latest_data(sid,data):
    sio.emit('latest_data',get_updated_list(),sid)

#================ When Device Disconnected =====================
@sio.event
def disconnect(sid):
    if sid in camera_list:
        print('\n================')
        print('== Disconnect ==',)
        print('================')
        print('camera no.',camera_list[sid]," disconnected")

        save_log(f" camera {camera_list[sid]['id']}"," Disconnected")
        camera_list.pop(sid)
        sio.emit('latest_data',get_updated_list())
        print_latest_list()
    elif sid in mobile_device_list:
        print('\n================')
        print('== Disconnect ==',)
        print('================')
        print('mobile device no.',mobile_device_list[sid]," disconnected")

        save_log(f" mobile device {mobile_device_list[sid]['id']}"," Disconnected")
        mobile_device_list.pop(sid)
        sio.emit('latest_data',get_updated_list())
        print_latest_list()        
    # elif sid in panel_list:
    #     print('\n================')
    #     print('== Disconnect ==',)
    #     print('================')
    #     print('panel no.',panel_list[sid]," disconnected")

    #     panel_list.pop(sid)
    #     sio.emit('latest_data',get_updated_list())
    #     print_latest_list()

    else:
        print("\n==Undefined Device Disconnected==")

#=================== Mobile Device's Event ====================
@sio.event
def cancel_alarm(sid, data):
    for i in camera_list:
        if camera_list[i]['id'] == data['camera_id']:
            

            print('\n======================')
            print('=== Alarm Canceled ===')
            print('======================')
            print('camera_id:',data['camera_id'])

            save_log(f" tablet {mobile_device_list[sid]['id']}",f" Canceled camera {camera_list[i]['id']} - {camera_list[i]['state']}")
            camera_list[i]['state'] = 'connected'
            sio.emit('latest_data',get_updated_list())
            send_to_panel(latest_LED())

            print_latest_list()
            break
    
#=================== Camera's Alarm Events ====================

@sio.event
def yellow_alarm(sid, data):
    camera_list[sid]['state']='yellow_alarm'
    sio.emit('latest_data',get_updated_list())
    sio.emit('yellow_alarm',{'camera_id':camera_list[sid]['id']})

    print('\n======================')
    print('===! Yellow Alarm !===')
    print('======================')
    print('camera_id:',camera_list[sid]['id'])

    save_log(f" camera {camera_list[sid]['id']}"," Yellow Alarm")
    send_to_panel(latest_LED())

    bibi_yellow_alarm_action()

    print_latest_list()

@sio.event
def red_alarm(sid, data):
    camera_list[sid]['state']='red_alarm'
    sio.emit('latest_data',get_updated_list())
    sio.emit('red_alarm',{'camera_id':camera_list[sid]['id']})

    print('\n=======================')
    print('===!!! Red Alarm !!!===')
    print('=======================')
    print('camera_id:',camera_list[sid]['id'])

    save_log(f" camera {camera_list[sid]['id']}"," Red Alarm")
    send_to_panel(latest_LED())
    bibi_red_alarm_action()
    print_latest_list()
#========= Functions==========

def print_latest_list():
        
        print('\n========= Latest lists ==========')

        print('----- Panel list -----')
        temp_panel_list = sorted(list(panel_list.values()),key=lambda dict: dict['id'])
        for mobile in temp_panel_list:
            print(mobile['type'], mobile['id'],mobile['state']) 

        print('----- Mobile Device list -----')
        temp_mobile_device_list = sorted(list(mobile_device_list.values()),key=lambda dict: dict['id'])
        for mobile in temp_mobile_device_list:
            print(mobile['type'], mobile['id'],mobile['state'])        

        print('----- Cameras list -----')
        temp_camera_list = sorted(list(camera_list.values()),key=lambda dict: dict['id'])
        for camera in temp_camera_list:
            print(camera['type'],camera['id'],camera['state'])
        

def get_updated_list():
    data={
        "camera":sorted(list(camera_list.values()),key=lambda dict: dict['id']),
        "mobile_device":sorted(list(mobile_device_list.values()),key=lambda dict: dict['id']),
        "panel":sorted(list(panel_list.values()),key=lambda dict: dict['id']),
        }
    return  data

def latest_LED():
    led = ["G","G","G","G","G","G","G","G",]

    camera_to_LED = {"7":2,
                 "9":1,
                 "11":0,
                 "47":7,
                 "45":6,
                 "43":5,
                 "41":4,
                 "38":3}

    for sid in camera_list:
        led_index = camera_to_LED[f"{camera_list[sid]['id']}"]
        if camera_list[sid]["state"] == "yellow_alarm":
            led[led_index] = "B"
        elif camera_list[sid]["state"] == "red_alarm":
            led[led_index] = "R"
    
    output = {"LED":led}
    return json.dumps(output)

def save_log(id,message):

    dt = datetime.now()
    file_name = f"./log/{dt.year}-{dt.month}-{dt.day}.txt"

    with open(file_name, "a") as log:
        log.write(f"{dt},{id},{message}\n")

def panel_register(panel_id):
    panel_list[panel_id] = {"id":panel_id,"state":"connected","type":"panel"}
    print(panel_list)
    sio.emit('latest_data',get_updated_list())
    print_latest_list()

def panel_deregister(panel_id):
    panel_list.pop(panel_id)
    print(panel_list)
    sio.emit('latest_data',get_updated_list())

    
def bibi_yellow_alarm_action():
    #actions here
    print('bibi yellow triggered')

def bibi_red_alarm_action():
    #actions here
    print('bibi red triggered')

#=================== Start SocketIO Server ====================

def central_server_start(port):
    print('== Socket Server Start ==')
    save_log(" central server"," Started")
    eventlet.wsgi.server(eventlet.listen(('', port)), app,log_output=False)

if __name__ =='__main__':
    central_server_start(12000)



# while True:
#     try:
#         print('==Socket Server Start==')
#         # print('Address: ',socket.gethostbyname_ex(socket.gethostname())[-1],' Prot: ',server_port)
#         eventlet.wsgi.server(eventlet.listen(('', server_port)), app,log_output=False)

#         break
#     except BaseException as error:
#         print(error,'\n\ninit server failed, re-trying')
#     time.sleep(0.5)
    


