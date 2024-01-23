# pip install "python-socketio[client]"

import socketio

device_type = "camera"
device_id = 999
socket_sever = ""

#rack_list = {rack_id : [layer1_state,layer2:state.....]} , states: green_state,yellow_state,red_state,unknown.
#layers from bottom to top, 0=bottom layer
rack_list = {
    1:[['unknown','unknown'], ['unknown','unknown'], ['unknown','unknown'], ['unknown','unknown']],
    2:[['unknown','unknown'], ['unknown','unknown'], ['unknown','unknown'], ['empty','empty']],
    }

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
            print(f"\n == Got Error on Connection Initialize ==\n{error}\nWill retry after 3s.")
        sio.sleep(3)   

    sio.wait()

#each call update 1 rack only.
# new rack state ----> {1:'green_state',2:'yellow_state',3:'red_state',4:'unknown'...}
def update_rack(rack_id,new_rack_state):
    global rack_list   
    rack_list[rack_id] = new_rack_state
    while True:        
        try:
            sio.emit('update_rack_state',{'rack_id':str(rack_id),'rack_state':rack_list[rack_id]})
            break
        except:
            print('re-trying, update rack state')
            sio.sleep(1)
    
def update_rack_raw(rs):
    state = {
        '0':'green_state',
        '1':'yellow_state',
        '2':'red_state',
    }

    rack1 = [[state[str(rs[0])],state[str(rs[1])]],
             [state[str(rs[4])],state[str(rs[5])]],
             [state[str(rs[8])],state[str(rs[9])]],
             [state[str(rs[12])],state[str(rs[13])]],             
             ]
    
    rack2 = [[state[str(rs[2])],state[str(rs[3])]],
             [state[str(rs[6])],state[str(rs[7])]],
             [state[str(rs[10])],state[str(rs[11])]],             
             ['empty','empty']
             ]
    
    while True:        
        try:
            sio.emit('update_rack_state',{'rack_id':'1','rack_state':rack1})
            sio.emit('update_rack_state',{'rack_id':'2','rack_state':rack2})
            break
        except:
            print('re-trying, update rack state')
            sio.sleep(2)


#=====================Socket IO Events===========================

@sio.event
def connect():
    print('== Server Connected ==')
    sio.emit("register",{"device_type":device_type,"device_id":device_id,"rack":rack_list})
    
@sio.event
def disconnect():
    print('== Server Disconnected ==')

@sio.event
def take_photo():
    #not yet done this part

    #sio.emit('send_photo',{})
    return


if __name__ == '__main__':
    connect_server(88,"ws://localhost:12000")






