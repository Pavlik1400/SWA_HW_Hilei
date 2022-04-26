import sys
import hazelcast as hz
sys.path.append("..")
from utils import N


if __name__ == '__main__':
    client = hz.HazelcastClient()
    q = client.get_queue("q")

    i = 0
    # while True:
    for i in range(N):
        print(f"Put {i}")
        q.put(i).result()
        # i += 1
