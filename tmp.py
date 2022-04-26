import subprocess

HZ_START_PATH = "./hz/bin/start.sh"

proc = subprocess.Popen(HZ_START_PATH)
print("hello, world")

proc.wait()