import hazelcast
import subprocess


HZ_START_PATH = "./hz/bin/start.sh"


class HazelcasInstancetWrapper:
    def __init__(self, hz_proc):
        self.hz_proc: subprocess.Popen = hz_proc
        self.hz_client = hazelcast.HazelcastClient()

    def get_map(self, name: str):
        return self.hz_client.get_map(name)

    def __del__(self):
        # make sure instance is dead
        self.hz_proc.terminate()

    @staticmethod
    def newHazelCastInstance():
        proc = subprocess.Popen(HZ_START_PATH)
        return HazelcasInstancetWrapper(hz_proc=proc)

