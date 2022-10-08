import bluepy 
import sys
from picamera import PiCamera
import os
import datetime
import time

device = "8C:4B:14:15:9E:16"
serviceUUID = "86f548d6-c323-479e-bbc7-defbcf190cd3"
sensorUUID = "6d58fd7e-dfd1-48e3-a1aa-508a37674586"
messageUUID = "9e3a3fe6-8887-4165-86ac-214c79b17cf2"

camFolder = "./camVid"

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

def main():
    connected = False
    # Connect to device
    while not (connected):
        try:
            server = bluepy.btle.Peripheral(device)
            print("a")
            connected = True
        except:
            pass

    #Get service and characteristic
    service = server.getServiceByUUID(serviceUUID)
    sensor = service.getCharacteristics(sensorUUID)[0]
    message = service.getCharacteristics(messageUUID)[0]

    #Get sensor value
    # while(1):
    human = int.from_bytes(sensor.read(), byteorder=sys.byteorder)
    print(human)
    if(human):
        camera()

main()
