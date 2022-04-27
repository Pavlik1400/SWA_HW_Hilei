import json
import random
import uuid
from typing import Tuple

import requests

from config import Config
from constants import DEFAULT_CONFIG_PATH
from logs import LOGGER


class FacadeService:
    def __init__(self, cnf_path: str = DEFAULT_CONFIG_PATH):
        self.config = Config.from_cnf_path(cnf_path)

    def add_message(self, text: str):
        LOGGER.info(f"FACADE: add_message({text})")
        logging_data = {
            "uuid": str(uuid.uuid1()),
            "message": text.strip("\"")
        }
        logging_data = json.dumps(logging_data)
        logging_uri = random.choice(self.config.logging_uri)
        requests.post(logging_uri, data=logging_data)

    def get_messages(self) -> Tuple[int, str]:
        LOGGER.info("FACADE: get_messages()")
        logging_uri = random.choice(self.config.logging_uri)
        logging_response = requests.get(logging_uri)
        messages_response = requests.get(self.config.message_uri)

        if logging_response.status_code != 200:
            return logging_response.status_code, f"error in logging service: {logging_response.text}"
        elif messages_response.status_code != 200:
            return messages_response.status_code, f"error in message service: {messages_response.text}"

        return 200, f"{logging_response.text}: {messages_response.text}"
