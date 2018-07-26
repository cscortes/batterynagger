import platform
import time
from enum import Enum

from lib.Nag import nag
from lib.PConfig import thePConfig
from lib.projlog import log
from lib.win_batteryinfo import win_battery_info


class BatteryLevel(Enum):
    NORMAL              = 5
    OK_BATTERY_CHARGING = 10
    WARNING             = 15
    CRITICAL            = 25
    FATAL               = 35

    def get_label(self):
        return str(self.name).capitalize().replace("_", " ")

class BatteryState(Enum):
    DISCHARGING = 0
    CHARGING    = 1

    def __str__(self):
        return str(self.name).capitalize().replace("_", " ")

class NoticeLogic(object):
    _emergency_power_flag = False

    def __init__(self):
        self.update_battery_info()

    def update_battery_info(self):
        if platform.system() == "Linux":
            from lib.myexec import exec, exec_lower

            self._percent = int(exec("cat","/sys/class/power_supply/BAT0/capacity"))
            status = exec_lower("cat","/sys/class/power_supply/BAT0/status")
            self._ischarging = BatteryState.CHARGING if (status == "charging") else BatteryState.DISCHARGING

        elif platform.system() == "Windows":
            self._percent, status = win_battery_info()
            self._ischarging = BatteryState.CHARGING if status else BatteryState.DISCHARGING

        else:
            self._percent, self._ischarging = (0, BatteryState.DISCHARGING)
            
    def get_percent(self):
        return self._percent

    def get_ischarging(self):
        return str(self._ischarging)

    def get_delay(self):
        return self._stime

    def get_level(self):
        if (self._ischarging == BatteryState.CHARGING):
            return BatteryLevel.OK_BATTERY_CHARGING

        if (self._percent <= thePConfig.get_fatal_level()):
            return BatteryLevel.FATAL

        elif (self._percent <= thePConfig.get_critical_level()):
            return BatteryLevel.CRITICAL

        elif (self._percent <= thePConfig.get_warning_level()):
            return BatteryLevel.WARNING

        return BatteryLevel.NORMAL

    def get_notification(self):
        return self.get_level().get_label()

    def should_sleep(self):
        self.update_battery_info()

        if self._ischarging == BatteryState.CHARGING:
            NoticeLogic._emergency_power_flag = False
        else:
            self.play_sound_warranted()

        self._stime = self.set_sleep_time()
        log.debug( "percent [{}%] time [{}s] charging: [{}]".format(
            self._percent, self._stime, self._ischarging))

        return True

    def set_sleep_time(self):
        n = self.get_level()
        return {
            BatteryLevel.NORMAL:                thePConfig.get_normal_timeout(),
            BatteryLevel.OK_BATTERY_CHARGING:   thePConfig.get_normal_timeout(),
            BatteryLevel.WARNING:               thePConfig.get_warning_timeout(),
            BatteryLevel.CRITICAL:              thePConfig.get_critical_timeout(),
            BatteryLevel.FATAL:                 thePConfig.get_fatal_timeout(),
        }.get(n, 1)

    def play_sound_warranted(self):
        n = self.get_level()        

        if (n == BatteryLevel.FATAL) and (NoticeLogic._emergency_power_flag == False):
            NoticeLogic._emergency_power_flag = True
            nag.play_emergency()
        
        elif (n in [BatteryLevel.WARNING, BatteryLevel.CRITICAL, BatteryLevel.FATAL] ):
            nag.play_notice()

    def sleep(self):
        time.sleep(self._stime)

if __name__ == "__main__":
    prog = NoticeLogic()

    while (True):
        if (prog.should_sleep()):
            prog.sleep()
