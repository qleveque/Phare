from bleak import BleakClient

ESP32_ADDRESS = "64:E8:33:88:6F:DE"
CHARACTERISTIC_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"

class MyBleClient:
    def __init__(self):
        self.address = ESP32_ADDRESS
        self.client = BleakClient(ESP32_ADDRESS)

    async def __aenter__(self):
        await self.client.connect()
        if not self.client.is_connected:
            raise ConnectionError(f"Failed to connect to {self.address}")
        print(f"Connected to {self.address}")
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.client.is_connected:
            await self.client.disconnect()
            print(f"Disconnected from {self.address}")

    async def send(self, message):
            encoded_data = message.encode("utf-8")
            await self.client.write_gatt_char(CHARACTERISTIC_UUID, encoded_data)
            print(f"Sent: {message}")
