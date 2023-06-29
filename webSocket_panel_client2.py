
import json
import asyncio
import websockets
import time

server = "ws://192.168.50.8:8888/panel_1"
# server = "ws://192.168.50.5:81"


async def trigger():
    
    await asyncio.sleep(2)
    # time.sleep(2)
    return json.dumps({"LED":["R","G","G","G","G","G","G","G"]})



async def receiver(websocket):
    try:
        async for message in websocket:
            print(message)
    # except websockets.ConnectionClosed:
    except BaseException as e:
        print('receiver error : ',e)

async def sender(websocket):
    while True:
        message = await trigger()
        try:
            await websocket.send(message)
        except BaseException as e:
            print('sender error : ',e)
            break
async def check_closed(websocket):
    await websocket.wait_closed()
    print("disconnected")

async def connect():
    async for websocket in websockets.connect(server):
        await asyncio.gather(sender(websocket),receiver(websocket),check_closed(websocket))

def websocket_start():
    asyncio.run(connect())

if __name__ == "__main__":
    websocket_start()