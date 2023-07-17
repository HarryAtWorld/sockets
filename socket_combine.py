from threading import Thread
import asyncio
import websockets

from socketio_server import central_server_start,api_hook,save_log,panel_register,panel_deregister,panel_cancel_all_alarm
from webSocket_panel_client2 import websocket_client_start

panel_1_ip = "ws://192.168.1.102:81/panel_1"
panel_2_ip = "ws://192.168.50.6:81/panel_2"
panel_3_ip = "ws://localhost:8888/panel_3"
central_server_port = 12000


panel_client1 = Thread(target = websocket_client_start,args=[panel_1_ip,1,api_hook,save_log,panel_register,panel_deregister,panel_cancel_all_alarm])
panel_client2 = Thread(target = websocket_client_start,args=[panel_2_ip,2,api_hook,save_log,panel_register,panel_deregister,panel_cancel_all_alarm])
panel_client3 = Thread(target = websocket_client_start,args=[panel_3_ip,1,api_hook,save_log,panel_register,panel_deregister,panel_cancel_all_alarm])
cental_server = Thread(target = central_server_start, args = [12000])


print("== socket_combine start ==")
panel_client3.start()
# panel_client2.start()
# panel_client1.start()
cental_server.start()

panel_client3.join()

# websocket.start()