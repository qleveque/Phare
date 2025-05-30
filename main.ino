#include <Arduino.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <Stepper.h>

#include <Stepper.h>
// TODO: is this correct ?
#define STEPS 200

#define DIRECTION 7
#define STEP 8

#define SPEED 50


Stepper stepper(STEPS, DIRECTION, STEP);

#define SERVICE_UUID        "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
#define CHARACTERISTIC_UUID "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"

class BluetoothCallback : public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic *pCharacteristic) {
        String receivedData = pCharacteristic->getValue().c_str();
        if (receivedData.length() > 0) {
            Serial.print("Received: ");
            Serial.println(receivedData);
            stepper.step(receivedData.toInt());
        }
    }
};

void setup() {
    Serial.begin(115200);
    Serial.println("Starting BLE...");
    stepper.setSpeed(SPEED);


    BLEDevice::init("ESP32-C3_BLE");
    BLEServer *pServer = BLEDevice::createServer();
    BLEService *pService = pServer->createService(SERVICE_UUID);
    BLECharacteristic *pCharacteristic = pService->createCharacteristic(
        CHARACTERISTIC_UUID,
        BLECharacteristic::PROPERTY_WRITE
    );

    pCharacteristic->setCallbacks(new BluetoothCallback());
    pService->start();
    BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
    pAdvertising->addServiceUUID(SERVICE_UUID);
    pAdvertising->setScanResponse(false);
    pAdvertising->setMinPreferred(0x06);
    pAdvertising->setMaxPreferred(0x12);
    pAdvertising->start();

    String macAddress = BLEDevice::getAddress().toString().c_str();
    Serial.print("ESP32 MAC Address: ");
    Serial.println(macAddress);

    Serial.println("BLE Ready. Waiting for data...");
}

void loop() {
    BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
    pAdvertising->start();
    delay(3000);
}

