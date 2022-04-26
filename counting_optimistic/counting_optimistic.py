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
    # m = client.get_map("map").blocking()
    m = client.get_map("map")
    key = "1"

    m.put_if_absent(key, Value()).result()
    # m.put_if_absent(key, Value())

    for k in range(N):
        debug and k % 100 == 0 and print(f"At: {k}")
        while True:
            oldValue: Value = m.get(key).result()
            # oldValue: Value = m.get(key)
            if oldValue is None:
                continue
            newValue = Value(oldValue)
            time.sleep(0.01)
            newValue.amount += 1
            if m.replace_if_same(key, oldValue, newValue).result():
                break

    print(f"Process {n} finished with {m.get(key).result().amount}")
    # print(f"Process {n} finished with {m.get(key).amount}")
