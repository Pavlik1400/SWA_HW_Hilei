import json
import random
import uuid
from typing import Tuple

import consul
import requests
from kafka import KafkaProducer

# from config import Config
from constants import DEFAULT_KAFKA_CONFIG, LOGGING, MESSAGES, KAFKA_CONFIG_KEY
from logs import LOGGER
from utils import get_or_set_default_consul, deserealize


class FacadeService:
    def __init__(self):
        self.c = consul.Consul()
        self.kafka_config = get_or_set_default_consul(self.c, key=KAFKA_CONFIG_KEY, default=DEFAULT_KAFKA_CONFIG)
        self.msg_producer = KafkaProducer(bootstrap_servers=self.kafka_config['uri'])

    def __sample_uri(self, service: str):
        uris = deserealize(self.c.kv.get(service)[1]['Value'].decode('ascii'))
        return random.choice(list(uris.values()))

    def add_message(self, text: str):
        LOGGER.info(f"FACADE: add_message({text})")
        msg = text.strip("\"")
        logging_data = json.dumps({
            "uuid": str(uuid.uuid1()),
            "message": msg
        })
        h = self.msg_producer.send(self.kafka_config['topic'], msg.encode('utf-8'))

        # now get loggine uris from consul, not config
        logging_uri = self.__sample_uri(LOGGING)

        requests.post(logging_uri, data=logging_data)
        h.get(timeout=10)
        self.msg_producer.flush()

    def get_messages(self) -> Tuple[int, str]:
        LOGGER.info("FACADE: get_messages()")
        logging_uri = self.__sample_uri(LOGGING)
        logging_response = requests.get(logging_uri)
        message_uri = self.__sample_uri(MESSAGES)
        messages_response = requests.get(message_uri)

        if logging_response.status_code != 200:
            return logging_response.status_code, f"error in logging service: {logging_response.text}"
        elif messages_response.status_code != 200:
            return messages_response.status_code, f"error in message service: {messages_response.text}"

        return 200, f"{logging_response.text}: {messages_response.text}"
