import hazelcast


def check_data_1000_lost(verbose=True):
    """returns number of lost entries"""
    m = client.get_map("m1").blocking()
    lost_counter = 0
    for i in range(1000):
        lost_counter += int(m.get(i) is None)
    if verbose:
        print(f"Lost {lost_counter}/{1000} entries")
    return lost_counter


if __name__ == '__main__':
    client = hazelcast.HazelcastClient()
    m = client.get_map("m1").blocking()

    for i in range(1000):
        m.put(i, f"v: {i}")
