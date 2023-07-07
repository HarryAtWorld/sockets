
import json
import asyncio
import websockets
import time

# server = "ws://192.168.50.8:8888/panel_1"
# server = "ws://192.168.50.5:81"


async def receiver(websocket,panel_id,log_callback,panel_register):

    try:
        async for message in websocket:
            if message == '{"Buzzer":"FALSE"]}':
                log_callback(f" panel {panel_id}"," Buzzer stopped")
            elif message == "Connected":
                print("eee")
                print(panel_id)
                panel_register(panel_id)
            print({message})

    except BaseException as e:
        print('receiver error : ',e)


async def sender(websocket):

    try:
        await websocket.send('{"LED":["G","G","G","G","G","G","G","G"]}')
    except BaseException as e:
        print('sender error : ',e)


async def check_closed(websocket, panel_id,log_callback,panel_deregister):
    await websocket.wait_closed()
    panel_deregister(panel_id)
    log_callback(f" panel {panel_id}"," Disconnected")
    print(f"panel {panel_id} disconnected")

async def connect(server_ip,panel_id,api_hook,log_callback,panel_register,panel_deregister):
    async for websocket in websockets.connect(server_ip):
        api_hook(websocket,panel_id)
        log_callback(f" panel {panel_id}"," Connected")
        await asyncio.gather(receiver(websocket,panel_id,log_callback,panel_register),check_closed(websocket,panel_id,log_callback,panel_deregister))

def websocket_client_start(server_ip ,panel_id, api_hook,log_callback,panel_register,panel_deregister):
   asyncio.run(connect(server_ip ,panel_id, api_hook,log_callback,panel_register,panel_deregister))

if __name__ == "__main__":
    def hook_for_test(input,id):
        return

    websocket_client_start("ws://192.168.1.100:81/panel_ttt","999",hook_for_test,hook_for_test)