import bluepy 
import sys

device = "8C:4B:14:15:9E:16"
serviceUUID = "86f548d6-c323-479e-bbc7-defbcf190cd3"
sensorUUID = "6d58fd7e-dfd1-48e3-a1aa-508a37674586"
messageUUID = "9e3a3fe6-8887-4165-86ac-214c79b17cf2"

def main():
    connected = False
    # Connect to device
    while not (connected):
        try:
            server = bluepy.btle.Peripheral(device)
            connected = True
        except:
            pass

    #Get service and characteristic
    service = server.getServiceByUUID(serviceUUID)
    sensor = service.getCharacteristics(sensorUUID)[0]
    message = service.getCharacteristics(messageUUID)[0]

    #Get sensor value
    human = int.from_bytes(sensor.read(), byteorder=sys.byteorder)
    

main()
