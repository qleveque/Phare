#!python.exe
import multiprocessing

from ble_client import MyBleClient
from shelly_dimmer import set_light
from audio_worker import audio_worker, play, stop, play_wait, set_volume


import asyncio
from asyncio import sleep

async def connect_and_send_messages(audio):
    async with MyBleClient() as client:
        async def turn(value):
            play(audio, "./sounds/gear.wav", loop=True, volume=0.5)
            await client.send(value)
            stop(audio, "./sounds/gear.wav")

        play(audio, "./sounds/music.wav", loop=True, volume=0.5)
        await turn("800")
        set_volume(audio, "./sounds/music.wav", 0.7)
        await play_wait(audio, "./sounds/audio0.wav")
        set_light(50)
        
        await turn("-1200")
        set_volume(audio, "./sounds/music.wav", 0.9)
        await play_wait(audio, "./sounds/audio1.wav")
        set_light(100)
        
        await turn("700")
        set_volume(audio, "./sounds/music.wav", 1)
        await play_wait(audio, "./sounds/audio2.wav")
        set_light(10)

        
        await sleep(0.5)
        set_light(100)
        await sleep(0.5)
        set_light(10)
        await sleep(0.5)
        set_light(100)
        
        await turn("-600")
        await play_wait(audio, "./sounds/audio3.wav")
        set_light(10)
        await sleep(0.5)
        set_light(100)
        await turn("300")

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    audio = multiprocessing.Queue()
    audio_process = multiprocessing.Process(target=audio_worker, args=(audio,))
    audio_process.start()

    asyncio.run(connect_and_send_messages(audio))

    audio.put({"action": "quit"})
