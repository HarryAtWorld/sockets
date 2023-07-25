import websockets
import asyncio

async def check_closed(websocket):
    await websocket.wait_closed()
    print("disconnected")

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


async def handler(websocket, path):
    print("### ",path," connected ###")
    await asyncio.gather(sender(websocket,"websocket connected"),receiver(websocket),check_closed(websocket))

with websockets.sync.serve(handler,  '', 8889) as server:
    server.serve_forever()