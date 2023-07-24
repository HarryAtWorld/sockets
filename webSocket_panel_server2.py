
import time
import asyncio
import websockets

camera_list = {}#Data Example: {camera_1 : {id:1, state:'connected',type:'camera'},........}
mobile_device_list = {} #Data Example: {Ejh3gs6d8SHG8 : {id:1, state:'connected',type:'mobile_device'},........}
panel_list = {}#Data Example: {panel_1:<websocket object>}

# sample message ==> {"event":"disconnection","data":{"id":1,"state":1,"type":1}}
def get_updated_list():
        data={
        "camera":sorted(list(camera_list.values()),key=lambda dict: dict['id']),
        "mobile_device":sorted(list(mobile_device_list.values()),key=lambda dict: dict['id']),
        "panel":sorted(list(panel_list.values()),key=lambda dict: dict['id']),
        }
        return  data 


async def register(websocket,data):
    match data["type"]:
        case "camera" :
            camera_list[f"camera_{data['id']}"] = {"id":data["id"],"state":data["state"],"type":data["type"]}
        case "mobile_device": 
            mobile_device_list[f"mobile_device_{data['id']}"] = {"id":data["id"],"state":data["state"],"type":data["type"]}
        case "panel":
            panel_list[f"panel_{data['id']}"] = {"id":data["id"],"state":data["state"],"type":data["type"]}

    try:
        await websocket.send()
    except BaseException as e:
        print(e)
    

async def disconnect(data):
     match data["type"]:
        case "camera" :
            camera_list.pop(f"camera_{data['id']}")
        case "mobile_device":
            mobile_device_list.pop(f"mobile_device_{data['id']}")
        case "panel":
            panel_list.pop(f"panel_{data['id']}")
    


async def yellow_alarm(data):
    camera_list[f"camera_{data['id']}"]["state"] = "yellow_alarm"


async def red_alarm(data):
    camera_list[f"camera_{data['id']}"]["state"] = "red_alarm"


async def event_action(message):
    match message["event"]:
        case "register": await register(message["data"])
        case "disconnection": await disconnect()
        case "yellow_alarm": await yellow_alarm()
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


async def handler(websocket, path):
    print("### ",path," connected ###")
    await asyncio.gather(sender(websocket,"websocket connected"),receiver(websocket),check_closed(websocket))


asyncio.get_event_loop().run_until_complete(websockets.serve(handler, '', 8889))
asyncio.get_event_loop().run_forever()

# websockets.serve(handler, '', 8888)
# asyncio.run()
