import configparser

class PConfig(object):
    LEVEL = "LEVEL"
    TIMEOUT = "TIMEOUT"

    def __init__(self, filename):
        self.filename = filename
        self.cnf = configparser.ConfigParser()
        self.cnf.read(self.filename)

    # Getter/Setter for LEVEL

    def get_fatal_level(self):
        return  int(self.cnf[PConfig.LEVEL].get("fatal","10"))
    def get_critical_level(self):
        return  int(self.cnf[PConfig.LEVEL].get("critical","20"))
    def get_warning_level(self):
        return  int(self.cnf[PConfig.LEVEL].get("warning","30"))

    def set_fatal_level(self, val):
        self.cnf.set(PConfig.LEVEL,"fatal",str(val))
    def set_critical_level(self, val):
        self.cnf.set(PConfig.LEVEL,"critical",str(val))
    def set_warning_level(self, val):
        self.cnf.set(PConfig.LEVEL,"warning",str(val))

    # Getter/Setter for timeout

    def get_fatal_timeout(self):
        return  int(self.cnf[PConfig.TIMEOUT].get("fatal","1"))
    def get_critical_timeout(self):
        return  int(self.cnf[PConfig.TIMEOUT].get("critical","4"))
    def get_warning_timeout(self):
        return  int(self.cnf[PConfig.TIMEOUT].get("warning","60"))
    def get_normal_timeout(self):
        return  int(self.cnf[PConfig.TIMEOUT].get("warning","120"))

    def set_fatal_timeout(self, val):
        self.cnf.set(PConfig.TIMEOUT,"fatal",str(val))
    def set_critical_timeout(self, val):
        self.cnf.set(PConfig.TIMEOUT,"critical",str(val))
    def set_warning_timeout(self, val):
        self.cnf.set(PConfig.TIMEOUT,"warning",str(val))
    def set_normal_timeout(self, val):
        self.cnf.set(PConfig.TIMEOUT,"normal",str(val))

    def update(self):
        with open(self.filename,"w") as f:
            self.cnf.write(f)

thePConfig = PConfig("nagger.cnf")
