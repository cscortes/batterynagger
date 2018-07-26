import sys
import os
from lib.projlog import log 
import pygame

class Nag(object):
    NOTICE_SOUND = "ping.ogg"
    EMERGENCY_POWER_SOUND = "low_bat.wav"

    def __init__(self):
        pygame.init()

        self.exit_if_not_found(Nag.NOTICE_SOUND)
        self.exit_if_not_found(Nag.EMERGENCY_POWER_SOUND)
        self.setup()

    def setup(self):
        ping_fname = os.path.join("sounds",Nag.NOTICE_SOUND)
        self.ping = pygame.mixer.Sound(file = ping_fname)
        self.ping.set_volume(1)

        voice_fname = os.path.join("sounds",Nag.EMERGENCY_POWER_SOUND)
        self.voice = pygame.mixer.Sound(file = voice_fname)
        self.voice.set_volume(1)
        
    def exit_if_not_found(self, fname):
        fname = os.path.join("sounds",fname)
        if (not os.path.exists(fname)):
            log.info("Sound file [{}] not found.".format(fname))
            sys.exit("Sound file [{}] not found.".format(fname))

    def play_notice(self):
        self.ping.play()

    def play_emergency(self):
        self.voice.play()
        
# really we only need 1 nag
#
nag = Nag()
