import json
import random
import uuid
from typing import Tuple

import requests
from kafka import KafkaProducer

from config import Config
from constants import DEFAULT_CONFIG_PATH, KAFKA_MSG_TOPIC, KAFKA_URI
from logs import LOGGER


class FacadeService:
    def __init__(self, cnf_path: str = DEFAULT_CONFIG_PATH):
        self.config = Config.from_cnf_path(cnf_path)
        self.msg_producer = KafkaProducer(bootstrap_servers=KAFKA_URI)

    def add_message(self, text: str):
        LOGGER.info(f"FACADE: add_message({text})")
        msg = text.strip("\"")
        logging_data = json.dumps({
            "uuid": str(uuid.uuid1()),
            "message": msg
        })
        h = self.msg_producer.send(KAFKA_MSG_TOPIC, msg.encode('utf-8'))
        logging_uri = random.choice(self.config.logging_uri)
        requests.post(logging_uri, data=logging_data)
        metadata = h.get(timeout=10)
        print(metadata.topic)
        print(metadata.partition)
        print(metadata.offset)
        self.msg_producer.flush()

    def get_messages(self) -> Tuple[int, str]:
        LOGGER.info("FACADE: get_messages()")
        logging_uri = random.choice(self.config.logging_uri)
        logging_response = requests.get(logging_uri)
        message_uri = random.choice(self.config.message_uri)
        messages_response = requests.get(message_uri)

        if logging_response.status_code != 200:
            return logging_response.status_code, f"error in logging service: {logging_response.text}"
        elif messages_response.status_code != 200:
            return messages_response.status_code, f"error in message service: {messages_response.text}"

        return 200, f"{logging_response.text}: {messages_response.text}"
