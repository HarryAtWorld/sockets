from threading import Thread
import asyncio
import websockets

from socketio_server import central_server_start,api_hook,save_log,panel_register,panel_deregister,panel_cancel_all_alarm,stp,latest_LED
from webSocket_panel_client2 import websocket_client_start
from socketio_auto_request import start_auto_request

panel_1_ip = "ws://192.168.1.110:81/panel_1"
panel_2_ip = "ws://192.168.1.111:81/panel_2"
panel_3_ip = "ws://localhost:8888/panel_3"
central_server_port = 12000


panel_client1 = Thread(target = websocket_client_start,args=[panel_1_ip,1,api_hook,save_log,panel_register,panel_deregister,panel_cancel_all_alarm,stp,latest_LED])
panel_client2 = Thread(target = websocket_client_start,args=[panel_2_ip,2,api_hook,save_log,panel_register,panel_deregister,panel_cancel_all_alarm,stp,latest_LED])
panel_client3 = Thread(target = websocket_client_start,args=[panel_3_ip,1,api_hook,save_log,panel_register,panel_deregister,panel_cancel_all_alarm,stp,latest_LED])
cental_server = Thread(target = central_server_start, args = [12000])
auto_request_machine = Thread(target = start_auto_request, args = [998,"ws://192.168.1.60:12000"])



print("== socket_combine start ==")
panel_client2.start()
panel_client1.start()

cental_server.start()
auto_request_machine.start()



panel_client2.join()
panel_client1.join()

# websocket.start()
