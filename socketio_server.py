#pip install python-socketio
#pip install eventlet

import eventlet
import socketio
import asyncio
from datetime import datetime
import os

camera_list = {} #Data Example: {Ejh3gs6d8SHG8 : {id:1, state:'connected',type:'camera'}, JD2ij24IJ2dbi5 : {id:2, state:'yellow_alarm',type:'camera'}}
mobile_device_list = {} #Data Example: same as camera list


#=============== log directory checking===================================
if not os.path.exists("./log/"):
    os.makedirs("./log/") 

#=============== SocketIO Setting ===================================

sio = socketio.Server(logger=False,engineio_logger=False,async_mode='eventlet')
app = socketio.WSGIApp(sio)


#================ When Device Connection Started ================
@sio.event
def connect(sid, environ):
    print_heading('Connection Created')
    print('new device socket ID:',sid)

#================ Devices Register =======================
@sio.event
def register(sid, data):    
    if data["device_type"] == 'camera': 
        camera_list[sid] = {'id':data["device_id"],'state':'connected','type':data["device_type"]}
        sio.emit('latest_data',get_updated_list())
        save_log(f" camera {camera_list[sid]['id']}"," Connected")

        print_heading('Camera Registered')
        print("camera no.",data["device_id"],",",' internal socket ID:',sid)
        print_latest_list()

    elif data['device_type'] == 'mobile_device':
        
        mobile_device_list[sid] = {'id':data["device_id"],'state':'connected','type':data["device_type"]}
        sio.emit('latest_data',get_updated_list())
        
        save_log(f" mobile device {mobile_device_list[sid]['id']}"," Connected")

        print_heading('Mobile Device Registered')
        print("mobile device no.",data["device_id"],",",' internal socketID: ',sid)
        print_latest_list()

request_count = 1

@sio.event
def request_latest_data(sid,data):
    global request_count
    sio.emit('latest_data',get_updated_list())
    print(f"=============================== auto send out latest data - counter: {request_count}======================================")
    request_count +=1
    if request_count >1000:
        request_count = 1

#================ When Device Disconnected =====================
@sio.event
def disconnect(sid):
    if sid in camera_list:
        print_heading('Camera Disconnected')
        print('camera no.',camera_list[sid]," disconnected")

        save_log(f" camera {camera_list[sid]['id']}"," Disconnected")
        try:
            camera_list.pop(sid)
        except:
            print('camera sid already deleted')
        sio.emit('latest_data',get_updated_list())
        print_latest_list()
    elif sid in mobile_device_list:
        print_heading('Mobile Device Disconnected')
        print('mobile device no.',mobile_device_list[sid]," disconnected")

        save_log(f" mobile device {mobile_device_list[sid]['id']}"," Disconnected")
        try:
            mobile_device_list.pop(sid)
        except:
            print("mobile devices sid already deleted")
        sio.emit('latest_data',get_updated_list())
        
        print_latest_list()

    else:
        print("\n==Undefined Device Disconnected==")

#=================== Mobile Device's Event ====================
@sio.event
def cancel_alarm(sid, data):
    for i in camera_list:
        if camera_list[i]['id'] == data['camera_id']:            

            print_heading('Alarm Canceled')
            print('camera_id:',data['camera_id'])

            save_log(f" Tablet {mobile_device_list[sid]['id']}",f" canceled camera {camera_list[i]['id']} - {camera_list[i]['state']}")
            camera_list[i]['state'] = 'connected'
            sio.emit('latest_data',get_updated_list())

            print_latest_list()
            break
    
#=================== Camera's Alarm Events ====================

@sio.event
def yellow_alarm(sid, data):
    camera_list[sid]['state']='yellow_alarm'
    sio.emit('latest_data',get_updated_list())
    sio.emit('yellow_alarm',{'camera_id':camera_list[sid]['id']})

    print_heading('!! Yellow Alarm !!')
    print('camera_id:',camera_list[sid]['id'],' in yellow alarm!')

    save_log(f" camera {camera_list[sid]['id']}"," Yellow Alarm")
    print_latest_list()

@sio.event
def red_alarm(sid, data):
    camera_list[sid]['state']='red_alarm'
    sio.emit('latest_data',get_updated_list())
    sio.emit('red_alarm',{'camera_id':camera_list[sid]['id']})

    print_heading('!!! Red Alarm !!!')
    print('camera_id:',camera_list[sid]['id'],' in red alarm!')

    save_log(f" camera {camera_list[sid]['id']}"," Red Alarm")
    print_latest_list()
#========= Functions==========

def print_latest_list():        
        print('\n========= Latest lists ==========')

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
        }
    return  data


def save_log(id,message):

    dt = datetime.now()
    file_name = f"./log/{dt.year}-{dt.month}-{dt.day}.txt"

    with open(file_name, "a") as log:
        log.write(f"{dt},{id},{message}\n")

def print_heading(heading):
    count = len(heading)
    print('\n')
    for i in range(count - 1+8):
        print("=",end='')
    print("=")
    print('=== {} ==='.format(heading))
    for i in range(count -1 +8):
        print("=",end='')
    print("=")


#=================== Start SocketIO Server ====================

def central_server_start(port):
    print('== Socket Server Start ==')
    save_log(" central server"," Started")
    eventlet.wsgi.server(eventlet.listen(('', port)), app,log_output=False)

if __name__ =='__main__':
    central_server_start(12000)



