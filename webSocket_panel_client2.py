
import json
import asyncio
import websockets
import time

# server = "ws://192.168.50.8:8888/panel_1"
# server = "ws://192.168.50.5:81"


async def receiver(websocket):
    try:
        async for message in websocket:
            print(message)

    except BaseException as e:
        print('receiver error : ',e)

async def sender(websocket):

    try:
        await websocket.send("####### Connected to Panel #######")
    except BaseException as e:
        print('sender error : ',e)


async def check_closed(websocket):
    await websocket.wait_closed()
    print("disconnected")

async def connect(ip,api_to_central,panel_id):
    async for websocket in websockets.connect(ip):

        api_to_central(websocket,panel_id)
        
        await asyncio.gather(sender(websocket),receiver(websocket),check_closed(websocket))

def websocket_client_start(ip , api_to_cental_server,panel_id):
   asyncio.run(connect(ip , api_to_cental_server,panel_id))

if __name__ == "__main__":
    def for_test(input):
        return

    websocket_client_start("ws://192.168.50.8:8888/panel_1",for_test)