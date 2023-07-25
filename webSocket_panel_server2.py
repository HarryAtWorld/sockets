
import time
import asyncio
import websockets
import json

camera_list = {}#Data Example: {camera_1 : {id:1, state:'connected',type:'camera'},........}
mobile_device_list = {} #Data Example: {mobile_device_1 : {id:1, state:'connected',type:'mobile_device'},........}
panel_list = {}#Data Example: {panel_1:{id:1, state:'connected',type:'panel'}}
panel_connection_list ={}#Data Example: {panel_1:<websocket object>, mobile_device_1:<websocket object>}
mobile_device_connection_list ={}

# sample message ==> {"event":"disconnection","data":{"id":1,"state":1,"type":1}}
def get_updated_list():
        data={
        "camera":sorted(list(camera_list.values()),key=lambda dict: dict['id']),
        "mobile_device":sorted(list(mobile_device_list.values()),key=lambda dict: dict['id']),
        "panel":sorted(list(panel_list.values()),key=lambda dict: dict['id']),
        }
        return  data
def latest_LED():
    led = ["E","E","E","E","E","E","E","E",]

    camera_to_LED = {"7":2,
                 "9":1,
                 "11":0,
                 "47":7,
                 "45":6,
                 "43":5,
                 "41":4,
                 "38":3}

    for camera in camera_list:
        led_index = camera_to_LED[f"{camera_list[camera]['id']}"]
        if camera_list[camera]["state"] == "connected":
            led[led_index] = "G"
        elif camera_list[camera]["state"] == "yellow_alarm":
            led[led_index] = "B"
        elif camera_list[camera]["state"] == "red_alarm":
            led[led_index] = "R"
    
    output = {"LED":led}
    return json.dumps(output)

async def send(connection,message):
    try:
        await connection.send(message)
    except BaseException as e:
            print('sender error : ',e)

async def send_to_all(event,data,target):
    global panel_connection_list
    global mobile_device_connection_list

    # match target:
    #     case "panel": connection_list = panel_connection_list
    #     case "mobile_device": connection_list = mobile_device_connection_list

    if target == "mobile_device":
        connection_list = mobile_device_connection_list
        message = json.dumps({"event":event,"data":data})
        connections = [send(connection_list[connection],message) for connection in connection_list]
        await asyncio.gather(*connections)
    elif target == "panel":
        connection_list = panel_connection_list
        message = data
        connections = [send(connection_list[connection],message) for connection in connection_list]
        await asyncio.gather(*connections)



async def register(websocket,data):
    match data["type"]:
        case "camera" :
            camera_list[f"camera_{data['id']}"] = {"id":data["id"],"state":data["state"],"type":data["type"]}
            await send_to_all("latest_data",get_updated_list(),"mobile_device")
            await send_to_all("latest_data",latest_LED(),"panel")
        case "mobile_device": 
            mobile_device_list[f"mobile_device_{data['id']}"] = {"id":data["id"],"state":data["state"],"type":data["type"]}
            mobile_device_connection_list[f"mobile_device_{data['id']}"] = websocket
            await send_to_all("latest_data",get_updated_list(),"mobile_device")
        case "panel":
            panel_list[f"panel_{data['id']}"] = {"id":data["id"],"state":data["state"],"type":data["type"]}
            panel_connection_list[f"panel_{data['id']}"] = websocket
            await send_to_all("latest_data",get_updated_list(),"mobile_device")
    

async def disconnect(data):
     match data["type"]:
        case "camera" :
            camera_list.pop(f"camera_{data['id']}")
            await send_to_all("latest_data",get_updated_list(),"mobile_device")
            await send_to_all("latest_data",latest_LED(),"panel")
        case "mobile_device":
            mobile_device_list.pop(f"mobile_device_{data['id']}")
            mobile_device_connection_list.pop(f"mobile_device_{data['id']}")
            await send_to_all("latest_data",get_updated_list(),"mobile_device")
        case "panel":
            panel_list.pop(f"panel_{data['id']}")
            panel_connection_list.pop(f"panel_{data['id']}")
            await send_to_all("latest_data",get_updated_list(),"mobile_device")
    


async def yellow_alarm(data):
    camera_list[f"camera_{data['id']}"]["state"] = "yellow_alarm"
    await send_to_all("latest_data",get_updated_list(),"mobile_device")
    await send_to_all("latest_data",latest_LED(),"panel")


async def red_alarm(data):
    camera_list[f"camera_{data['id']}"]["state"] = "red_alarm"
    await send_to_all("latest_data",get_updated_list(),"mobile_device")
    await send_to_all("latest_data",latest_LED(),"panel")

async def cancel_alarm(data,cid):
    camera_list[f"camera_{data['id']}"]["state"] = "connected"
    await send_to_all("latest_data",get_updated_list(),"mobile_device")
    await send_to_all("latest_data",latest_LED(),"panel")

async def cancel_all_alarm(data,cid):
    for i in camera_list:
        if not camera_list[i]["state"] == "disconnected":
            camera_list[i]["state"] = "connected"
    await send_to_all("latest_data",get_updated_list(),"mobile_device")
    await send_to_all("latest_data",latest_LED(),"panel")




async def event_action(message):
    match message["event"]:
        case "Connected":print ("connected")
        case "register": await register(message["data"])
        case "disconnection": await disconnect()
        case "yellow_alarm": await yellow_alarm(message["data"])
        case "red_alarm":await red_alarm()        
        case "cancel_alarm":await cancel_alarm()
        case "cancel_all_alarms": await cancel_all_alarm()  





async def sender(websocket,message):
        try:
            await websocket.send(message)
        except BaseException as e:
            print("sender error : ",e)

async def receiver(websocket):    

        async for message in websocket:
            try:
                # await asyncio.sleep(2)
                print(message)
                await sender(websocket,"@@ res from server @@")
            except BaseException as e:
                print("receiver error : ",e)


async def check_closed(websocket):
    await websocket.wait_closed()
    print("disconnected")


async def handler(websocket, connection_id):
    connection_id = connection_id[1:]

    print("### ",connection_id," connected ###")
    await asyncio.gather(sender(websocket,"websocket connected"),receiver(websocket),check_closed(websocket))


asyncio.get_event_loop().run_until_complete(websockets.serve(handler, '', 8889))
asyncio.get_event_loop().run_forever()

# websockets.serve(handler, '', 8888)
# asyncio.run()
