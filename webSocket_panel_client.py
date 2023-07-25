
import json
import asyncio
import websockets
import time

# server = "ws://192.168.50.8:8888/panel_1"
server = "ws://192.168.88.24:81/camera_1"

connection = None



async def receiver(websocket):
    async for message in websocket:
        try:
            print(message)
    # except websockets.ConnectionClosed:
        except BaseException as e:
            print('receiver error : ',e)

async def sender(message):
    global connection
    await connection.send(message)

def yellow_alarm():
    asyncio.run(sender(json.dumps({'event':"yellow_alarm","data":id})))


    
async def check_closed(websocket):
    await websocket.wait_closed()
    print("disconnected")

async def connect():
    async for websocket in websockets.connect(server):
        try:
            global connection
            connection = websocket
            await asyncio.gather(receiver(websocket),check_closed(websocket))
        except websockets.ConnectionClosed:
            continue

def websocket_start():
    asyncio.run(connect())

if __name__ == "__main__":
    websocket_start()