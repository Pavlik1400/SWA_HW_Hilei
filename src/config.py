from typing import Dict, List, Union

import yaml
from constants import LOGGING, MESSAGES, FACADE, DEFAULT_CONFIG_PATH
from dataclasses import dataclass


@dataclass
class Config:
    facade_uri: str
    logging_uri: str
    message_uri: str

    @staticmethod
    def from_cnf_path(path: str = DEFAULT_CONFIG_PATH):
        config: Dict = yaml.load(open(path, 'r'), Loader=yaml.FullLoader)
        return Config(
            Config.__cnf_to_uri(config[FACADE]),
            Config.__cnf_to_uri(config[LOGGING]),
            Config.__cnf_to_uri(config[MESSAGES]),
        )

    @staticmethod
    def __cnf_to_uri(addr: Union[Dict, List[Dict]]) -> Union[List, str]:
        if isinstance(addr, list):
            return [f"http://{subaddr['host']}:{subaddr['port']}" for subaddr in addr]
        elif isinstance(addr, dict):
            return f"http://{addr['host']}:{addr['port']}"
        else:
            raise ValueError("Bad 'addr' type")

