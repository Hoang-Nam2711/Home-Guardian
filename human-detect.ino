#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <BLE2902.h>

static BLEUUID SERVICE_UUID("86f548d6-c323-479e-bbc7-defbcf190cd3");
static BLEUUID SENSOR_UUID("6d58fd7e-dfd1-48e3-a1aa-508a37674586");

const int sensor = 13;

BLEServer *pServer=NULL;
BLECharacteristic *pCharacteristic=NULL;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  pinMode(sensor,INPUT);

  Serial.println("Bluetooth init");

  //Create BLE Device
  BLEDevice::init("Human Detect");

  //Create Server
  pServer = BLEDevice::createServer();

  //Create Service
  BLEService *pService = pServer->createService(SERVICE_UUID);

  //Create Characteristic
  pCharacteristic = pService->createCharacteristic(
                                         SENSOR_UUID,
                                         BLECharacteristic::PROPERTY_READ|
                                         BLECharacteristic::PROPERTY_NOTIFY
                                       );
  pCharacteristic -> addDescriptor(new BLE2902());
  pService->start();
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  BLEDevice::startAdvertising();
}

void loop() {
  uint32_t sensorValue = digitalRead(sensor);
  pCharacteristic->setValue((uint8_t*)&sensorValue,1);
  pCharacteristic->notify();
  delay(1000);
}