from threading import Thread
import asyncio
import websockets

from socketio_server import socketio_start
from webSocket_panel_client2 import hello,websocket_start,ff


socketIO = Thread(target = socketio_start)
# websocket = Thread(target = websocket_start)
web_client = Thread(target=client)


print("== socket_combine start ==")


socketIO.start()
web_client.start()
# websocket.start()