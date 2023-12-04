const { io } = require("socket.io-client");
// import {io} from 'socket.io-client';

 const cameraList = [];
for (let i= 0; i < 8; i++) {
  cameraList[i] = {id: i + 1, state: 'disconnected',type:'camera'};
}

const mobileDeviceList = [];
for (let i = 0; i < 3; i++) {
  mobileDeviceList[i] = {id: i + 1, state: 'disconnected',type:'mobile_device'};
}

let device_type = "mobile_device"
let device_id = 2
let socket_sever = "ws://192.168.88.112:12000"

const socket = io(socket_sever);

socket.on("connect", () => {
    socket.emit("register", { device_type: device_type, device_id: device_id })
    console.log("====Server Connected====")
})

// socket.on("request_register",(data)=>{
//     socket.emit("register",{device_type:device_type,device_id:device_id})
//     console.log("==get register request from socket server==")
// })

socket.on("disconnect", () => {
    
    console.log("====Server Disconnected====")
})

socket.on('latest_data', (data) => {    
    cameraList.forEach(item => {
       item['state'] = 'disconnected' 
        for (let i of data['camera']) {
          if (item['id'] === i['id']) {
            item['state'] = i['state'];
          }
        }
      });
    
      mobileDeviceList.forEach(item => {
        item['state'] = 'disconnected'
        for (let i of data['mobile_device']) {
          if (item['id'] === i['id']) {
            item['state'] = i['state'];
          }
        }
      });

    console.log('====Got Latest Data====')
    console.log('=Camera List=')
    console.log(cameraList)
    console.log('=Mobile Device List=')
    console.log(mobileDeviceList);
});

socket.on('yellow_alarm', (data) => {
    cameraList.forEach(item => {
        if (item['id'] === data.camera_id) {
          item['state'] = 'yellow_alarm';
        }
      });
    console.log(`====! Got Yellow Alarm !====`)
    console.log(cameraList);
});

socket.on('red_alarm', (data) => {
    cameraList.forEach(item => {
        if (item['id'] === data.camera_id) {
          item['state'] = 'yellow_alarm';
        }
      });
    console.log(`====!!! Got Red Alarm !!!====`)
    console.log(cameraList);
});


setInterval(() => { }, 5000); //for keeping this programme running
