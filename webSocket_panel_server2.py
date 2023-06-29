#!/usr/bin/env python
import time
import asyncio
from websockets.server import serve

async def echo(websocket):
    async for message in websocket:
        await websocket.send("server received~~~")
        time.sleep(3)
        await  websocket.send("server received~~~2")
        print('from client: ', message)

async def main():
    async with serve(echo, "", 8888):

        await broadcast("gggg==")
        await asyncio.Future()  # run forever

async def test():
    print('before starting')
    for i in range(5):
        print('stop ', i)
        await asyncio.sleep(3)
    print('before starting 2')


asyncio.run(main())


# ==================================================

# import time
# import asyncio
# import websockets


# async def handler(websocket, path):
#     print('== Client Connected ==', path)

#     await websocket.send("hiiiiii")

#     try:
#         async for message in websocket:
#             print(message,'received from client')
#             res = f"this is server res : ~~~~~ {message}"

#             await websocket.send(res)
#             time.sleep(2)
#             await websocket.send("2nd res from server")
            
#             print(f"2nd res to client")
#     except websockets.ConnectionClosed:
#              print('== Client Disconnected ==')


# asyncio.get_event_loop().run_until_complete(websockets.serve(handler, '', 8888))
# asyncio.get_event_loop().run_forever()