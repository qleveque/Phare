#!python.exe
from time import sleep

from ble_client import MyBleClient
from shelly_dimmer import set_light
from sound import play_sound


import asyncio
from asyncio import sleep

async def connect_and_send_messages():
    async with MyBleClient() as client:
        await client.send("800")
        await asyncio.to_thread(play_sound, "./sounds/audio0.wav")
        set_light(50)
        
        await client.send("-1200")
        await asyncio.to_thread(play_sound, "./sounds/audio1.wav")
        set_light(100)
        
        await client.send("700")
        await asyncio.to_thread(play_sound, "./sounds/audio2.wav")
        set_light(10)
        
        await sleep(0.5)
        set_light(100)
        await sleep(0.5)
        set_light(10)
        await sleep(0.5)
        set_light(100)
        
        await client.send("-600")
        await asyncio.to_thread(play_sound, "./sounds/audio3.wav")
        set_light(10)
        await sleep(0.5)
        set_light(100)
        
        await client.send("300")

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(connect_and_send_messages())
