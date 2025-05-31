#include <Arduino.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>

#define DIR_PIN 7
#define STEP_PIN 8

#define SERVICE_UUID        "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
#define CHARACTERISTIC_UUID "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"

void turn(int steps, int delay) {
    if(steps < 0) {
        steps *= -1;
        digitalWrite(DIR_PIN, LOW);
    } else {
        digitalWrite(DIR_PIN, HIGH);
    }
    for (int i = 0; i < steps; i++) {
        digitalWrite(STEP_PIN, HIGH);
        delayMicroseconds(delay);
        digitalWrite(STEP_PIN, LOW);
        delayMicroseconds(delay);
    }
}

class BluetoothCallback : public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic *pCharacteristic) {
        String receivedData = pCharacteristic->getValue().c_str();
        if (receivedData.length() > 0) {
            Serial.print("Received: ");
            Serial.println(receivedData);

            int spaceIndex = receivedData.indexOf(' ');
            if (spaceIndex == -1) {
                Serial.println("Invalid format. Use: <steps> <delay>");
                return;
            }

            String stepsStr = receivedData.substring(0, spaceIndex);
            String delayStr = receivedData.substring(spaceIndex + 1);
            int steps = stepsStr.toInt();
            int delay = delayStr.toInt();

            turn(steps, delay);

            Serial.println("Stepper moved " + stepsStr + " steps with " + delayStr + " delay");
        }
    }
};

void setup() {
    Serial.begin(115200);
    Serial.println("Starting BLE...");

    pinMode(STEP_PIN, OUTPUT);
    pinMode(DIR_PIN, OUTPUT);

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
    delay(100)
}

