import os
import subprocess
from argparse import ArgumentParser, Namespace
from typing import Dict, Optional

import yaml

from src import FACADE, LOGGING, MESSAGES, CONTROLLERS

SERVICES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")


def main(args: Namespace, config: Dict, n: int):
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

    if isinstance(config[selected_service], list):
        host = config[selected_service][n]['host']
        port = config[selected_service][n]['port']
    else:
        host = config[selected_service]['host']
        port = config[selected_service]['port']

    start_cmd = f"{starter} {controller} --host {host} --port {port}"
    subprocess.run(start_cmd, shell=True)


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("--config", "-c", type=str, required=False, help="config with ports",
                        default="services_config.yml")
    parser.add_argument("--facade", action="store_const", const=True, help="start facade service")
    parser.add_argument("--logging", action="store_const", const=True, help="start logging service")
    parser.add_argument("--messages", action="store_const", const=True, help="start messages service")
    parser.add_argument("--number", "-n", type=int, required=False, default=0,
                        help="Number of service in case of replication")
    args = parser.parse_args()

    config: Dict = yaml.load(open(args.config, 'r'), Loader=yaml.FullLoader)

    try:
        os.chdir(SERVICES_PATH)
    except Exception as exc:
        print(f"Is main.py in right directory? \n{exc}")

    main(args, config, args.number)
