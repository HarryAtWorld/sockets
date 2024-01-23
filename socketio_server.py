#pip install python-socketio
#pip install eventlet

import socketio
import asyncio
from datetime import datetime
from aiohttp import web
import os
import json

camera_list = {} #Data Example: {Ejh3gs6d8SHG8 : {id:1, state:'connected',type:'camera'}, JD2ij24IJ2dbi5 : {id:2, state:'yellow_alarm',type:'camera'}}
ipad_list = {} #Data Example: same as camera list
smart_watch_list ={} #Data Example: same as camera list
rack_list = {}# {rack_id : [layer1_state,layer_state.....]}
camera_rack_match ={}# data framework  { camera_d : rack_id,.....}

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

    if type(data) == str:
        data = json.loads(data)

        if data['device_type'] == 'smart_watch':
            smart_watch_list[sid] = {'id':data["device_id"],'state':'connected','type':data["device_type"]}
            
            save_log(f" smart watch no. {smart_watch_list[sid]['id']}"," Connected")
            print_heading(f'Smart watch no. {data["device_id"]} Registered')

        else:
            print('<<< unknown device trying to register >>>')           


    elif data["device_type"] == 'camera': 
        camera_list[sid] = {'id':data["device_id"],'state':'connected','type':data["device_type"]}
        camera_rack_match[data["device_id"]] = []
        for rack_id in data['rack']:
            rack_list[rack_id] = data['rack'][rack_id]
            camera_rack_match[data["device_id"]].append(rack_id)

        save_log(f" camera {camera_list[sid]['id']}"," Connected")
        print_heading(f'Camera no. {data["device_id"]} Registered')
        
        
    elif data['device_type'] == 'ipad':        
        ipad_list[sid] = {'id':data["device_id"],'state':'connected','type':data["device_type"]}
                
        save_log(f" Ipad {ipad_list[sid]['id']}"," Connected")
        print_heading(f'Ipad no. {data["device_id"]} Registered')

    else:
        print('<<< unknown device trying to register >>>')
        

    await sio.emit('latest_data',get_updated_list())
    print_latest_list()



@sio.event
async def request_latest_data(sid,data):
    await sio.emit('latest_data',get_updated_list())


#================ When Device Disconnected =====================
@sio.event
async def disconnect(sid):
    global rack_list
    if sid in camera_list:
        print_heading(f"Camera no. {camera_list[sid]['id']} Disconnected")
        save_log(f" camera {camera_list[sid]['id']}"," Disconnected")
        
        
           
        rack_list = {
            '1':[['unknown','unknown'], ['unknown','unknown'], ['unknown','unknown'], ['unknown','unknown']],
            '2':[['unknown','unknown'], ['unknown','unknown'], ['unknown','unknown'], ['empty','empty']]
                
            }    
        
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
        print_heading(f"Smart watch no. {smart_watch_list[sid]['id']} Disconnected")
        save_log(f" smart watch no. {smart_watch_list[sid]['id']}"," Disconnected")
        try:
            smart_watch_list.pop(sid)
        except:
            print("smart watch sid already deleted")
        await sio.emit('latest_data',get_updated_list())
        
        print_latest_list()

    else:
        print("\n==Undefined Device Disconnected==")

#=================== Mobile Device's Event ====================
@sio.event
async def request_photo(sid, data):
    # not yet done this part

    # target camera id in data

    #sio.emit('take_photo',{},'< target camnera >')

    #reply by 'request_photo'
    
    return
#=================== Camera's Event ====================
@sio.event
async def send_photo(sid, data):

    # not yet done this part

    # target devices id in data

    return
            
    
#=================== Rack's State Events ====================
        
#rack_data = {'rack_id':1,'rack_state':['unknown','unknown',...]}
@sio.event
async def update_rack_state(sid, rack_data):

    print_heading('!! Rack State Updated !!')

    rack_id = rack_data['rack_id'] 
    rack_list[rack_id] = rack_data['rack_state'] 

    # rack_list[rack_data['rack_id']]=rack_data['rack_state']
    save_log(f" Rack {rack_id} ",f" new state: {rack_data['rack_state']}")

    print(f" Rack {rack_id} new state: {rack_data['rack_state']}")

    await sio.emit('latest_data',get_updated_list())
    print_latest_list()  


#========= Functions ==========

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
        
        print('-------- Rack List --------')
        temp_rack_list = sorted(list(rack_list.items()))
        for rack , state in temp_rack_list:
            print(f"rack {rack}, {state}")
        

def get_updated_list():  
    data={
        "camera":sorted(list(camera_list.values()),key=lambda dict: dict['id']),
        "ipad":sorted(list(ipad_list.values()),key=lambda dict: dict['id']),
        "smartWatch":sorted(list(smart_watch_list.values()),key=lambda dict: dict['id']),
        "rack":sorted(list(rack_list.items()))
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
    print_heading(' SocketIO Server Start ')
    save_log(" central server"," Started")
    web.run_app(app,port=port)

if __name__ =='__main__':
    central_server_start(12000)


