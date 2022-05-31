import threading

from fastapi import FastAPI
from kafka import KafkaConsumer

from constants import DEFAULT_KAFKA_CONFIG, KAFKA_CONFIG_KEY
import consul
from utils import get_or_set_default_consul
from logs import LOGGER

controller = FastAPI()

MSG_STORAGE = []


def msg_loop():
    cons = consul.Consul()
    kafka_cnf = get_or_set_default_consul(cons, key=KAFKA_CONFIG_KEY, default=DEFAULT_KAFKA_CONFIG)
    msg_consumer = KafkaConsumer(
        kafka_cnf['topic'],
        group_id='my-group0',
        bootstrap_servers=kafka_cnf['uri'],
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )
    for msg in msg_consumer:
        m = msg.value.decode()
        LOGGER.info(f"MESSAGE: Got message: {m}")
        MSG_STORAGE.append(m)


t = threading.Thread(target=msg_loop)
t.start()


@controller.get("/")
def get_messages():
    LOGGER.info("MESSAGES: get_messages()")
    print(MSG_STORAGE)
    return MSG_STORAGE
    # return "message-service is not implemented yet"
