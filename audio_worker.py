import pygame
import wave
import queue
from asyncio import sleep

def play(command_queue, path, loop=False, volume=1.0):
    command_queue.put({
        "action": "play_loop" if loop else "play_once",
        "path": path,
        "volume": volume
    })

async def play_wait(command_queue, path, volume=1.0):
    command_queue.put({
        "action": "play_once",
        "path": path,
        "volume": volume
    })
    with wave.open(path, "rb") as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration_seconds = frames / float(rate)
        await sleep(duration_seconds)

def stop(command_queue, path):
    command_queue.put({"action": "stop_loop", "path": path})

def set_volume(command_queue, path, volume):
    command_queue.put({
        "action": "set_volume",
        "path": path,
        "volume": volume
    })

def audio_worker(command_queue):
    pygame.mixer.init()
    print("Audio process started")

    # Dict to keep track of looping sounds and their channels: {path: (Sound, Channel, volume)}
    looping_sounds = {}

    while True:
        try:
            cmd = command_queue.get(timeout=0.1)
        except queue.Empty:
            continue

        if isinstance(cmd, dict):
            action = cmd.get("action")
            path = cmd.get("path")
            volume = cmd.get("volume", 1.0)

            if action == "play_loop" and path:
                # Stop if already playing this loop to restart cleanly
                if path in looping_sounds:
                    sound, channel, _ = looping_sounds[path]
                    channel.stop()
                sound = pygame.mixer.Sound(path)
                channel = sound.play(loops=-1)
                channel.set_volume(volume)
                looping_sounds[path] = (sound, channel, volume)
                print(f"Started looping sound: {path} with volume {volume}")

            elif action == "play_once" and path:
                sound = pygame.mixer.Sound(path)
                sound.set_volume(volume)
                sound.play()
                print(f"Played once sound: {path} with volume {volume}")

            elif action == "stop_loop" and path:
                if path in looping_sounds:
                    sound, channel, _ = looping_sounds[path]
                    channel.stop()
                    del looping_sounds[path]
                    print(f"Stopped looping sound: {path}")

            elif action == "set_volume" and path:
                if path in looping_sounds:
                    sound, channel, _ = looping_sounds[path]
                    if channel is not None:
                        print(f"Channel busy: {channel.get_busy()}")
                        channel.set_volume(volume)
                        looping_sounds[path] = (sound, channel, volume)
                        print(f"Set volume of looping sound {path} to {volume}")
                    else:
                        print(f"Warning: No active channel for {path}, cannot set volume")
                else:
                    print(f"Cannot set volume of looping sound {path}")

            elif action == "quit":
                # Stop all looping sounds cleanly
                for sound, channel, _ in looping_sounds.values():
                    channel.stop()
                looping_sounds.clear()
                print("Audio process quitting.")
                break

        elif cmd == "QUIT":
            for sound, channel, _ in looping_sounds.values():
                channel.stop()
            looping_sounds.clear()
            print("Audio process quitting.")
            break
