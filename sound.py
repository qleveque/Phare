import winsound

def play_sound(sound):
    winsound.PlaySound(sound, winsound.SND_FILENAME)

# # import pygame
# # pygame.mixer.init()
#
# # Store channels per sound
# sound_channels = {}
#
# def play_sound(file_path):
#     # sound_name = file_path
#     # sound = pygame.mixer.Sound(file_path)
#     # channel = sound.play()
#     # sound_channels[sound_name] = (sound, channel)
#     pass
#
# def stop(sound_name):
#     # if sound_name in sound_channels:
#     #     sound, channel = sound_channels[sound_name]
#     #     channel.stop()
#     #     del sound_channels[sound_name]
#     pass
