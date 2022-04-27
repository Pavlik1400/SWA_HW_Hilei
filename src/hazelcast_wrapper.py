import subprocess
import os

import hazelcast

HZ_START_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "hz", "bin", "start.sh")


class HazelcasInstancetWrapper:
    def __init__(self, hz_proc):
        self.hz_proc: subprocess.Popen = hz_proc
        self.hz_client = hazelcast.HazelcastClient()

    def get_map(self, name: str):
        return self.hz_client.get_map(name)

    def __del__(self):
        # make sure instance is dead
        self.hz_proc.terminate()


class HazelcastWrapper:
    @staticmethod
    def newHazelCastInstance() -> HazelcasInstancetWrapper:
        proc = subprocess.Popen(HZ_START_PATH)
        return HazelcasInstancetWrapper(hz_proc=proc)
