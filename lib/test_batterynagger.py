from bat_checker import NoticeLogic, EMERGENCY_POWER_SOUND, NOTICE_SOUND

import pytest

class subprocess:
    pass


class mymocksubprocess:
    
    def __init__(self):
        self.ccall = None
        self.cout = None
        self.pccall = None

    def check_call(self, mylist):
        print(id(self), mylist)
        self.pccall = self.ccall
        self.ccall = mylist 
        return mylist

    def check_output(self, mylist):
        print(id(self),mylist)
        self.cout = mylist
        return mylist

class TestPercent(object):

    def test_init(self):
        n = NoticeLogic()

        assert n.fatal_level == 1
        assert n.critical_level == 2
        assert n.warning_level == 3

    def test_only_1_time(self):
        mock = mymocksubprocess()
        mock2 = mymocksubprocess()
        mock3 = mymocksubprocess()
        NoticeLogic._emergency_power_flag = False

        n = NoticeLogic()
        n.subprocess = mock2

        assert NoticeLogic._emergency_power_flag == False
        n.play_emergency()

        assert NoticeLogic._emergency_power_flag == True
        assert mock2.ccall != None
        assert mock2.ccall[1] == EMERGENCY_POWER_SOUND

        n.subprocess = mock3
        n.play_emergency()
        assert mock3.ccall == None
        


class TestSleepTime(object):

    def test_fatal(self):
        n = NoticeLogic( )

        assert n.set_sleep_time(9) == 0
        assert n.set_sleep_time(11) != 0

    def test_critical(self):
        n = NoticeLogic( )

        assert n.set_sleep_time(19) == 2
        assert n.set_sleep_time(21) != 2

    def test_warning(self):
        n = NoticeLogic()

        assert n.set_sleep_time(29) == 60 * 4
        assert n.set_sleep_time(31) != 60 * 4

    def test_normal(self):
        n = NoticeLogic()

        assert n.set_sleep_time(31) == 60 *10

class TestWarrantedSound(object):

    def test_emergency(self):
        mock = mymocksubprocess()
        n = NoticeLogic()
        NoticeLogic._emergency_power_flag = False

        n.play_sound_warranted(9)
        assert n._emergency_power_flag == True
        assert mock.pccall != None
        assert mock.pccall[1] == EMERGENCY_POWER_SOUND

        assert mock.ccall != None
        assert mock.ccall[1] == NOTICE_SOUND


    def test_notice(self):
        mock = mymocksubprocess()
        n = NoticeLogic()

        n.play_sound_warranted(29)
        assert mock.ccall != None
        assert mock.ccall[1] == NOTICE_SOUND

    def test_normal(self):
        mock = mymocksubprocess()
        mock2 = mymocksubprocess()
        n = NoticeLogic()
        n.subprocess = mock2
        n.play_sound_warranted(31)
        assert mock2.ccall == None
