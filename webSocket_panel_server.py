# #!/usr/bin/env python
# import time
# import asyncio
# from websockets.server import serve

# async def echo(websocket):
#     async for message in websocket:
#         await websocket.send("server received~~~")
#         time.sleep(3)
#         await  websocket.send("server received~~~2")
#         print('from client: ', message)

# async def main():
#     async with serve(echo, "", 8888):
#         await asyncio.Future()  # run forever

# async def test():
#     print('before starting')
#     for i in range(5):
#         print('stop ', i)
#         await asyncio.sleep(3)
#     print('before starting 2')

# print('before starting')
# # asyncio.run(test())
# asyncio.run(main())
# print('after starting')

# ==================================================

import time
import asyncio
import websockets

async def sender(websocket,message):        
        try:
            await websocket.send(message)
        except BaseException as e:
            print("sender error : ",e)

async def receiver(websocket):    

    try:
        async for message in websocket:
            # await asyncio.sleep(2)
            print(message)
            await sender(websocket,"abc")
    except BaseException as e:
        print("receiver error : ",e)


async def check_closed(websocket):
    await websocket.wait_closed()
    print("disconnected")


async def handler(websocket, path):
    print("### ",path," connected ###")
    await asyncio.gather(sender(websocket,"Connected"),receiver(websocket),check_closed(websocket))


asyncio.get_event_loop().run_until_complete(websockets.serve(handler, '', 8888))
asyncio.get_event_loop().run_forever()

# websockets.serve(handler, '', 8888)
# asyncio.run()
