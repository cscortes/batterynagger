import logbook as LB
import sys 

LB.StreamHandler(sys.stdout).push_application()
log = LB.Logger("bat_checker")
