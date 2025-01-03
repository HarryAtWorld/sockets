#pip install python-socketio
#pip install aiohttp

import socketio
import asyncio
from datetime import datetime

from aiohttp import web
import os
import json

log_path = "/home/hkuit/sockets/log/"

computer_list = {
    1:{'id':1, 'state':'disconnected','type':'edge_computer'},
    2:{'id':2, 'state':'disconnected','type':'edge_computer'},
    3:{'id':3, 'state':'disconnected','type':'edge_computer'},
}

camera_list={
    1:{'id':1, 'state':'disconnected','type':'camera','alarms':[]},
    2:{'id':2, 'state':'disconnected','type':'camera','alarms':[]},
    3:{'id':3, 'state':'disconnected','type':'camera','alarms':[]},
    4:{'id':4, 'state':'disconnected','type':'camera','alarms':[]},

}

ipad_list={
    1:{'id':1, 'state':'disconnected','type':'ipad'},
    2:{'id':2, 'state':'disconnected','type':'ipad'},
    3:{'id':3, 'state':'disconnected','type':'ipad'},

}

watch_list={
    1:{'id':1, 'state':'disconnected','type':'smart_watch'},
    2:{'id':2, 'state':'disconnected','type':'smart_watch'},
    3:{'id':3, 'state':'disconnected','type':'smart_watch'},
}

camera_connection_list = {} # {socket_id : [camera_id,...]} --> Data Example: {Ejh3gs6d8SHG8 :[1,3,5,6.....]}
ipad_connection_list = {} # {socket_id : ipad_id} --> Data Example: {FsddsffhIU3:1,JHDYeEJjYGE:2,...}
watch_connection_list ={} #{socket_id : watch_id} --> Data Example: same as ipad connection list
computer_connection_list = {}#{socket_id : computer_id} --> Data Example: same as ipad connection list


#=============== log directory checking===================================
if not os.path.exists(log_path):
    os.makedirs(log_path) 

#=============== SocketIO Setting ===================================

sio = socketio.AsyncServer(async_mode='aiohttp',cors_allowed_origins='*')
app = web.Application()
# app = web.Application(middlewares=[cors_middleware(allow_all=True)])
# app = web.Application(
#     middlewares=[
#         cors_middleware(origins=["http://192.168.0.252"])
#     ]
# )


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
            watch_connection_list[sid] =  data['device_id']
            watch_list[data['device_id']]['state'] = 'connected'
            
            save_log(f" smart watch no. {data['device_id']}"," Connected")
            print_heading(f'Smart watch no. {data["device_id"]} Registered')

        else:
            print('<<< unknown device trying to register >>>')
            


    elif data["device_type"] == 'edge_computer':
        computer_connection_list[sid] = data['computer_id']
        computer_list[data['computer_id']]['state'] = 'connected'

        camera_connection_list[sid] = data['camera_list']

        #check if camera already connected

        for camera_id in data['camera_list']:
            if camera_list[camera_id]['state'] == 'disconnected' or camera_list[camera_id]['state'] =='error' :
                camera_list[camera_id]['state'] = 'connected'
                save_log(f" camera {camera_id}"," Connected")     
                
        print_heading(f'Camera no. {data["camera_list"]} Registered')  
        
        
    elif data['device_type'] == 'ipad':        
        ipad_connection_list[sid] = data['device_id']
        ipad_list[data['device_id']]['state'] = 'connected'
                
        save_log(f" Ipad {data['device_id']}"," Connected")
        print_heading(f'Ipad no. {data["device_id"]} Registered')

    else:
        print('<<< unknown device trying to register >>>')
        

    await sio.emit('latest_data',get_updated_list())
    print_latest_list()


@sio.event
async def request_latest_data(sid,data):
    await sio.emit('latest_data',get_updated_list())

# for event testing
@sio.event
async def hi(sid):
    print("receive hi")
    await sio.emit('bye')


#================ When Device Disconnected =====================
@sio.event
async def disconnect(sid):
    # if sid in camera_connection_list:
    if sid in computer_connection_list:
        # check if computer reconnected on other sid
        computer_id = computer_connection_list[sid]
        count = list(computer_connection_list.values()).count(computer_id)
        if count == 1:
            print_heading(f"Camera no. {camera_connection_list[sid]} Disconnected")
            save_log(f" camera {camera_connection_list[sid]}"," Disconnected")
            try:
                computer_list[computer_id]['state'] = 'disconnected'
                
                for camera_id in camera_connection_list[sid]:
                    camera_list[camera_id]['state'] = 'disconnected'     
                    camera_list[camera_id]['alarms'] = []                                               
            except:
                print('error on update camera/computer disconnect state')

        try:
            computer_connection_list.pop(sid)
            camera_connection_list.pop(sid)
        except:
            print('camera/computer connection sid already deleted')

        await sio.emit('latest_data',get_updated_list())
        print_latest_list()


    elif sid in ipad_connection_list:
        # check if ipad reconnected on other sid
        ipad_id = ipad_connection_list[sid]
        count = list(ipad_connection_list.values()).count(ipad_id)
        if count ==1:
            print_heading(f"Ipad no. {ipad_connection_list[sid]} Disconnected")
            save_log(f" ipad no. {ipad_connection_list[sid]}"," Disconnected")
            try:
                ipad_list[ipad_connection_list[sid]]['state'] = 'disconnected'                
            except:
                print("error on update ipad disconnect state")

        try:           
            ipad_connection_list.pop(sid)
        except:
            print("ipad sid already deleted")         
            
        await sio.emit('latest_data',get_updated_list())        
        print_latest_list()

    elif sid in watch_connection_list:
        # check if watch reconnected on other sid
        watch_id = watch_connection_list[sid]
        count = list(watch_connection_list.values()).count(watch_id)
        if count ==1 :            
            print_heading(f"Smart watch no. {watch_connection_list[sid]} Disconnected")
            save_log(f" smart watch no. {watch_connection_list[sid]}"," Disconnected")
            try:
                watch_list[watch_connection_list[sid]]['state'] = 'disconnected'                
            except:
                print("error on update smart watch disconnect state")

        try:            
            watch_connection_list.pop(sid)
        except:
            print("smart watch sid already deleted")


        await sio.emit('latest_data',get_updated_list())   
        print_latest_list()

    else:
        print("\n==Undefined Device Disconnected==")

#=================== Mobile Device's Event ====================
@sio.event
async def cancel_alarm(sid, data):

    if camera_list[data['camera_id']]['state'] == 'disconnected':
        print('!!! Cancel Fail - alarmed camera already offline!!!')
        return
    if camera_list[data['camera_id']]['state'] == 'connected':
        print('!!! Cancel Fail -  camera not in alarm !!!')
        return
    
    print_heading('Alarm Canceled')    

    if ipad_connection_list.get(sid,None):
        print('camera_id:',data['camera_id'], ' by ',f" ipad {ipad_list[ipad_connection_list[sid]]['id']}")

        save_log(f" ipad {ipad_list[ipad_connection_list[sid]]['id']}",f" canceled camera {data['camera_id']} - {camera_list[data['camera_id']]['state']}")
    else :
        print('camera_id:',data['camera_id'])
        save_log(f" camera {data['camera_id']}",f" {camera_list[data['camera_id']]['state']} canceled ")
    camera_list[data['camera_id']]['state'] = 'connected'
    await sio.emit('latest_data',get_updated_list())

    print_latest_list()

@sio.event
async def cancel_alarm_location(sid, data):
    #data sample--> {camera_id:"1","alarm":[x,y,'red_alarm']}

    if not data['alarm'] in camera_list[data['camera_id']]['alarms']:
        return
    
    print_heading('Alarm Location Canceled')
    print('camera_id:',data['camera_id'],data['alarm'])

    save_log(f"camera {data['camera_id']}" , f" {data['alarm']} canceled ")

    camera_list[data['camera_id']]['alarms'] = list(filter(lambda i: not (i[0] == data['alarm'][0] and i[1] == data['alarm'][1] and i[2] == data['alarm'][2]),camera_list[data['camera_id']]['alarms']))
    await sio.emit('latest_data',get_updated_list())

    print_latest_list()
            
    
#=================== Camera's Alarm Events ====================

@sio.event
async def yellow_alarm(sid, data):
    if camera_list[data['camera_id']]['state']=='red_alarm':
        print('--- camera already on red alarm ---')
        return
    
    camera_list[data['camera_id']]['state']='yellow_alarm'
    await sio.emit('yellow_alarm',{'camera_id':data['camera_id']})
    await sio.emit('latest_data',get_updated_list())

    print_heading('!! Yellow Alarm !!')
    print('camera_id:',data['camera_id'],' in yellow alarm!')

    save_log(f" camera {data['camera_id']}"," Yellow Alarm")
    print_latest_list()

@sio.event
async def red_alarm(sid, data):
    camera_list[data['camera_id']]['state']='red_alarm'
    await sio.emit('red_alarm',{'camera_id':data['camera_id']})
    await sio.emit('latest_data',get_updated_list())

    print_heading('!!! Red Alarm !!!')
    print('camera_id:',data['camera_id'],' in red alarm!')

    save_log(f" camera {data['camera_id']}"," Red Alarm")
    print_latest_list()

#!!!!!!!!!!! Not ready for use !!!!!!!!!
@sio.event
async def alarm_location(sid, data):   

    if data['alarm'] in camera_list[data['camera_id']]['alarms']:
        print('duplicated')
        return

    camera_list[data['camera_id']]['alarms'].append(data['alarm'])
    
    await sio.emit('latest_data',get_updated_list())

    print_heading('!!! Alarm !!!')
    print('camera_id:',data['camera_id'],' in ',data['alarm'])

    save_log(f" camera {data['camera_id']}",f"{data['alarm']}")
    print_latest_list()

@sio.event
async def camera_error(sid, data):
    camera_list[data['camera_id']]['state']='error'
    await sio.emit('camera_error',{'camera_id':data['camera_id']})
    await sio.emit('latest_data',get_updated_list())

    print_heading('!!! Camera Error!!!')
    print('camera_id:',data['camera_id'],' in error!')

    save_log(f" camera {data['camera_id']}"," Error")
    print_latest_list()

@sio.event
async def camera_blocked(sid, data):
    camera_list[data['camera_id']]['state']='blocked'
    await sio.emit('camera_blocked',{'camera_id':data['camera_id']})
    await sio.emit('latest_data',get_updated_list())

    print_heading('!!! Camera Blocked !!!')
    print('camera_id:',data['camera_id'],' is blocked!')

    save_log(f" camera {data['camera_id']}"," Blocked")
    print_latest_list()

@sio.event
async def camera_resumed(sid, data):
    camera_list[data['camera_id']]['state']='connected'
    # await sio.emit('camera_resumed',{'camera_id':data['camera_id']})
    await sio.emit('latest_data',get_updated_list())

    print_heading('!!! Camera Resumed!!!')
    print('camera_id:',data['camera_id'],' resumed!')

    save_log(f" camera {data['camera_id']}"," Camera Resumed")
    print_latest_list()
#========= Functions==========

def print_latest_list():        
        print('<<<<<<   Latest Lists   >>>>>>')

        print('----- Mobile Device List -----')        
        for id in ipad_list:
            if ipad_list[id]['state'] != 'disconnected':
                print(ipad_list[id]['type'], ipad_list[id]['id'],ipad_list[id]['state'])

        print('------ Smart Watch List ------')        
        for id in watch_list:
            if watch_list[id]['state'] != 'disconnected':
                print(watch_list[id]['type'], watch_list[id]['id'],watch_list[id]['state'])      

        print('-------- Cameras List --------')        
        for id in camera_list:
            if camera_list[id]['state'] != 'disconnected':
                print(camera_list[id]['type'],camera_list[id]['id'],camera_list[id]['state'],camera_list[id]['alarms'])
        

def get_updated_list():
    data={
        "cameras":list(camera_list.values()),
        "ipads":list(ipad_list.values()),
        "smartWatches":list(watch_list.values()),
        }    
    return  data


def save_log(id,message):

    dt = datetime.now()
    file_name = f"{log_path}{dt.year}-{dt.month}-{dt.day}.txt"

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


