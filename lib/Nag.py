import sys
import os
from lib.projlog import log 
import subprocess
from lib.myexec import exec

class Nag(object):
    NOTICE_SOUND = "ping.mp3"
    EMERGENCY_POWER_SOUND = "low_bat.mp3"

    def __init__(self):
        self.exit_if_not_found(Nag.NOTICE_SOUND)
        self.exit_if_not_found(Nag.EMERGENCY_POWER_SOUND)
        
    def exit_if_not_found(self, fname):
        fname = os.path.join("sounds",fname)
        if (not os.path.exists(fname)):
            log.info("Sound file [{}] not found.".format(fname))
            sys.exit("Sound file [{}] not found.".format(fname))

    def play_notice(self):
        fname = os.path.join("sounds",Nag.NOTICE_SOUND)
        exec("play", fname)

    def play_emergency(self):
        fname = os.path.join("sounds",Nag.EMERGENCY_POWER_SOUND)
        exec("play",fname)


# really we only need 1 nag
#
nag = Nag()
