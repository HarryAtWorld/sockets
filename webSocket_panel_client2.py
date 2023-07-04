
import json
import asyncio
import websockets
import time

# server = "ws://192.168.50.8:8888/panel_1"
# server = "ws://192.168.50.5:81"

async def receiver(websocket,panel_id):
    try:
        async for message in websocket:
            print(f"panel {panel_id} got # {message} #")

    except BaseException as e:
        print('receiver error : ',e)

async def sender(websocket):

    try:
        await websocket.send("####### Connected to Panel #######")
    except BaseException as e:
        print('sender error : ',e)


async def check_closed(websocket, panel_id):
    await websocket.wait_closed()
    print(f"panel {panel_id} disconnected")

async def connect(ip,api_hook,panel_id):
    async for websocket in websockets.connect(ip):
        api_hook(websocket,panel_id)        
        await asyncio.gather(receiver(websocket,panel_id),check_closed(websocket,panel_id))

def websocket_client_start(ip , api_hook, panel_id):
   asyncio.run(connect(ip , api_hook, panel_id))

if __name__ == "__main__":
    def hook_for_test(input):
        return

    websocket_client_start("ws://192.168.50.8:8888/panel_1",hook_for_test,"999")