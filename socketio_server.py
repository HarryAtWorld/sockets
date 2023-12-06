#pip install python-socketio
#pip install eventlet

import socketio
import asyncio
from datetime import datetime
from aiohttp import web
import os

camera_list = {} #Data Example: {Ejh3gs6d8SHG8 : {id:1, state:'connected',type:'camera'}, JD2ij24IJ2dbi5 : {id:2, state:'yellow_alarm',type:'camera'}}
ipad_list = {} #Data Example: same as camera list
smart_watch_list ={} #Data Example: same as camera list


#=============== log directory checking===================================
if not os.path.exists("./log/"):
    os.makedirs("./log/") 

#=============== SocketIO Setting ===================================

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)

#================ When Device Connection Started ================
@sio.event
def connect(sid, environ):
    print_heading('Connection Created')
    print('new device socket ID:',sid)

#================ Devices Register =======================
@sio.event
async def register(sid, data):    
    if data["device_type"] == 'camera': 
        camera_list[sid] = {'id':data["device_id"],'state':'connected','type':data["device_type"]}
        
        save_log(f" camera {camera_list[sid]['id']}"," Connected")
        print_heading(f'Camera no. {data["device_id"]} Registered')  
        
    elif data['device_type'] == 'ipad':        
        ipad_list[sid] = {'id':data["device_id"],'state':'connected','type':data["device_type"]}
                
        save_log(f" ipad {ipad_list[sid]['id']}"," Connected")
        print_heading(f'Ipad no. {data["device_id"]} Registered')
        
    elif data['device_type'] == 'smartWatch':        
        smart_watch_list[sid] = {'id':data["device_id"],'state':'connected','type':data["device_type"]}
        
        save_log(f" smart watch no. {smart_watch_list[sid]['id']}"," Connected")
        print_heading(f'smart watch no. {data["device_id"]} Registered')

    await sio.emit('latest_data',get_updated_list())
    print_latest_list()



@sio.event
async def request_latest_data(sid,data):
    await sio.emit('latest_data',get_updated_list())


#================ When Device Disconnected =====================
@sio.event
async def disconnect(sid):
    if sid in camera_list:
        print_heading(f"Camera no. {camera_list[sid]['id']} Disconnected")
        save_log(f" camera {camera_list[sid]['id']}"," Disconnected")
        try:
            camera_list.pop(sid)
        except:
            print('camera sid already deleted')
        await sio.emit('latest_data',get_updated_list())
        print_latest_list()
    elif sid in ipad_list:
        print_heading(f"Ipad no. {ipad_list[sid]['id']} Disconnected")
        save_log(f" ipad no. {ipad_list[sid]['id']}"," Disconnected")
        try:
            ipad_list.pop(sid)
        except:
            print("ipad sid already deleted")
        await sio.emit('latest_data',get_updated_list())
        
        print_latest_list()
    elif sid in smart_watch_list:
        print_heading(f"Smart watch no. {ipad_list[sid]['id']} Disconnected")
        save_log(f" smart watch no. {smart_watch_list[sid]['id']}"," Disconnected")
        try:
            ipad_list.pop(sid)
        except:
            print("smart watch sid already deleted")
        await sio.emit('latest_data',get_updated_list())
        
        print_latest_list()

    else:
        print("\n==Undefined Device Disconnected==")

#=================== Mobile Device's Event ====================
@sio.event
async def cancel_alarm(sid, data):
    for i in camera_list:
        if camera_list[i]['id'] == data['camera_id']:

            print_heading('Alarm Canceled')
            print('camera_id:',data['camera_id'])

            save_log(f" Tablet {ipad_list[sid]['id']}",f" canceled camera {camera_list[i]['id']} - {camera_list[i]['state']}")
            camera_list[i]['state'] = 'connected'
            await sio.emit('latest_data',get_updated_list())

            print_latest_list()
            break
    
#=================== Camera's Alarm Events ====================

@sio.event
async def yellow_alarm(sid, data):
    camera_list[sid]['state']='yellow_alarm'
    await sio.emit('yellow_alarm',{'camera_id':camera_list[sid]['id']})
    await sio.emit('latest_data',get_updated_list())

    print_heading('!! Yellow Alarm !!')
    print('camera_id:',camera_list[sid]['id'],' in yellow alarm!')

    save_log(f" camera {camera_list[sid]['id']}"," Yellow Alarm")
    print_latest_list()

@sio.event
async def red_alarm(sid, data):
    camera_list[sid]['state']='red_alarm'
    await sio.emit('red_alarm',{'camera_id':camera_list[sid]['id']})
    await sio.emit('latest_data',get_updated_list())

    print_heading('!!! Red Alarm !!!')
    print('camera_id:',camera_list[sid]['id'],' in red alarm!')

    save_log(f" camera {camera_list[sid]['id']}"," Red Alarm")
    print_latest_list()
#========= Functions==========

def print_latest_list():        
        print('<<<<<<   Latest Lists   >>>>>>')

        print('----- Mobile Device List -----')
        temp_ipad_list = sorted(list(ipad_list.values()),key=lambda dict: dict['id'])
        for mobile in temp_ipad_list:
            print(mobile['type'], mobile['id'],mobile['state'])

        print('------ Smart Watch List ------')
        temp_smart_watch_list = sorted(list(smart_watch_list.values()),key=lambda dict: dict['id'])
        for watch in temp_smart_watch_list:
            print(watch['type'], watch['id'],watch['state'])      

        print('-------- Cameras List --------')
        temp_camera_list = sorted(list(camera_list.values()),key=lambda dict: dict['id'])
        for camera in temp_camera_list:
            print(camera['type'],camera['id'],camera['state'])
        

def get_updated_list():
    data={
        "camera":sorted(list(camera_list.values()),key=lambda dict: dict['id']),
        "ipad":sorted(list(ipad_list.values()),key=lambda dict: dict['id']),
        "smartWatch":sorted(list(ipad_list.values()),key=lambda dict: dict['id']),
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
    print('    {}    '.format(heading))
    for i in range(count -1 +8):
        print("=",end='')
    print("=")


#=================== Start SocketIO Server ====================

def central_server_start(port):
    print_heading('SocketIO Server Start')
    save_log(" central server"," Started")
    web.run_app(app,port=port)

if __name__ =='__main__':
    central_server_start(12000)


