import bluepy 
import sys
from picamera import PiCamera
import os
import datetime
import time
import asyncio
from variable import device,sensorUUID,serviceUUID

camFolder = "./camVid"
cycle = 1*60 #5 mins
lastUpdate = time.time()

def camSave():
    time = datetime.datetime.today()
    fileName = "humanDetect-"+str(time.day)+str(time.month)+str(time.year)+"-"+str(time.hour)+str(time.minute)+str(time.second)
    print(fileName)
    return camFolder + "/" + fileName  +".h264"

def camera():
    camera=PiCamera()
    camera.start_recording(camSave())
    time.sleep(60)
    camera.stop_recording()

def connectDevice():
    connected = False
    # Connect to device
    while not (connected):
        try:
            server = bluepy.btle.Peripheral(device)
            connected = True
        except:
            print("Trying...")
            pass

    #Get service and characteristic
    service = server.getServiceByUUID(serviceUUID)
    sensor = service.getCharacteristics(sensorUUID)[0]

    time.sleep(5); #wait 5 seconds for update connection
    human = int.from_bytes(sensor.read(), byteorder=sys.byteorder)
    print(human)
    if(human):
        camera()
        server.disconnect()
        
        
async def main(lastUpdate):
    while(1):
        if(time.time()-lastUpdate > cycle):
            print("A")
            connectDevice()
            lastUpdate = time.time()
            # lastUpdate = connectDevice()
            # print(lastUpdate)

loop = asyncio.get_event_loop()
loop.run_until_complete(main(lastUpdate))