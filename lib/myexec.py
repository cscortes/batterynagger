import subprocess

def exec(cmd, param):
    return  subprocess.check_output([cmd,param]).decode().strip()

def exec_lower(cmd, param):
    return  exec(cmd, param).lower()

