import hazelcast as hz
import time
from argparse import ArgumentParser
import sys

sys.path.append("..")
from utils import Value, N

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-n", required=True)
    parser.add_argument("-d", action="store_const", const=True)
    args = parser.parse_args()
    n = args.n
    debug = args.d

    client = hz.HazelcastClient()
    m = client.get_map("map")
    key = "1"

    # m.put("1", Value())
    m.put_if_absent(key, Value()).result()

    for k in range(N):
        debug and k % 100 == 0 and print(f"At: {k}")
        value: Value = m.get(key).result()
        time.sleep(0.01)
        value.amount += 1
        m.put(key, value).result()

    print(f"Process {n} finished with {m.get(key).result().amount}")
