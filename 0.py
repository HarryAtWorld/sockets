
import asyncio
import time

async def ok():
    while True:
        await asyncio.sleep(3)
        # time.sleep(1)

async def task():

    await ok()
    print("ok")

asyncio.run(task())
