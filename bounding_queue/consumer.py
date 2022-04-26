import sys
from argparse import ArgumentParser
import hazelcast as hz
sys.path.append("..")
from utils import N


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-n", required=True)
    args = parser.parse_args()
    n = args.n

    client = hz.HazelcastClient()
    q = client.get_queue("q")

    while True:
    # for i in range(N):
        v = q.poll().result()
        if v is None:
            continue
        print(f"Consumer {n} poll {v}")
