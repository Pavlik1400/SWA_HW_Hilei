import json
from typing import Any

from consul import Consul
# import os
# import sys
# sys.path.append(os.getcwd())
# from src.logs import LOGGER


def serialize(obj):
    return json.dumps(obj)


def deserealize(s):
    return json.loads(s)


def get_or_set_default_consul(cons: Consul, key: str, default: Any):
    print(f"[DEB] consul.get({key})")
    resp = cons.kv.get(key)[1]
    if resp is None:
        print(f"[DEB] consule.put({key}, {default}")
        cons.kv.put("msg-topic", serialize(default))
        return default
    return deserealize(resp.decode("ascii"))
