from threading import Thread
import asyncio
import websockets

from socketio_server import central_server_start,api_to_central
from webSocket_panel_client2 import websocket_client_start

panel_1_ip = "ws://192.168.50.8:8888/panel_1"
panel_2_ip = "ws://192.168.50.6:81/panel_2"
panel_3_ip = "ws://192.168.50.8:8889/panel_3"
central_server_port = 12000


panel_client1 = Thread(target = websocket_client_start,args=[panel_1_ip,api_to_central,"1"])
panel_client2 = Thread(target = websocket_client_start,args=[panel_2_ip,api_to_central,"2"])
panel_client3 = Thread(target = websocket_client_start,args=[panel_3_ip,api_to_central,"3"])
cental_server = Thread(target = central_server_start, args = [12000])


print("== socket_combine start ==")
panel_client3.start()
panel_client2.start()
panel_client1.start()
cental_server.start()

# websocket.start()