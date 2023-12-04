
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
            await sender(websocket,"@@ res from server @@")
    except BaseException as e:
        print("receiver error : ",e)


async def check_closed(websocket):
    await websocket.wait_closed()
    print("disconnected")


async def handler(websocket, path):
    print("### ",path," connected ###")
    await asyncio.gather(sender(websocket,"connected"),receiver(websocket),check_closed(websocket))


asyncio.get_event_loop().run_until_complete(websockets.serve(handler, '', 8889))
asyncio.get_event_loop().run_forever()

# websockets.serve(handler, '', 8888)
# asyncio.run()
