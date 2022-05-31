import os
import subprocess
from argparse import ArgumentParser, Namespace
from typing import Optional

import consul

from src import FACADE, LOGGING, MESSAGES, CONTROLLERS
from src.logs import LOGGER
from src.utils import serialize, deserealize

SERVICES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")


def main(args: Namespace):
    selected_service: Optional[str] = None
    if args.facade:
        if args.logging or args.messages:
            raise ValueError("Specify only one of --facade, --logging, --messages service to start")
        selected_service = FACADE
    elif args.logging:
        if args.messages:
            raise ValueError("Specify only one of --facade, --logging, --messages service to start")
        selected_service = LOGGING
    elif args.messages:
        selected_service = MESSAGES
    else:
        raise ValueError("Specify one of --facade, --logging, --messages service to start")

    # if there are many addresses, start the one with the given number(n)
    starter = "uvicorn"
    controller = f"{CONTROLLERS[selected_service]}:controller"

    start_cmd = f"{starter} {controller} --host {args.host} --port {args.port}"
    c = consul.Consul()
    # if n is None, then serive starts in one instance

    uri = f"http://{args.host}:{args.port}"
    if args.n is None:
        service_uri = serialize(uri)
        LOGGER.debug(f"consule.put({selected_service}, {service_uri})")
        c.kv.put(selected_service, service_uri)
    else:
        # if there is no list of uri, add it
        uris = c.kv.get(selected_service)[1]

        # if there is a dict, set value, else create new dict
        name_to_uri = {
            selected_service + f"_{args.n}": uri
        }
        if uris is None:
            service_uris = serialize(name_to_uri)
        else:
            current_uris = deserealize(uris['Value'].decode('ascii'))
            current_uris.update(name_to_uri)
            service_uris = serialize(current_uris)
        LOGGER.debug(f"consule.put({selected_service}, {service_uris})")
        c.kv.put(selected_service, service_uris)

    subprocess.run(start_cmd, shell=True)


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("--facade", action="store_const", const=True, help="start facade service")
    parser.add_argument("--logging", action="store_const", const=True, help="start logging service")
    parser.add_argument("--messages", action="store_const", const=True, help="start messages service")
    parser.add_argument("-n", type=int, required=False, default=None,
                        help="Number of service in case of replication")
    parser.add_argument("--host", type=str, default="localhost")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    try:
        os.chdir(SERVICES_PATH)
    except Exception as exc:
        print(f"Is main.py in right directory? \n{exc}")

    main(args)
