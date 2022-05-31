import threading

from fastapi import FastAPI
from kafka import KafkaConsumer

from constants import KAFKA_MSG_TOPIC, KAFKA_URI
from logs import LOGGER

controller = FastAPI()

MSG_STORAGE = []


def msg_loop():
    msg_consumer = KafkaConsumer(KAFKA_MSG_TOPIC,
                                 group_id='my-group0',
                                 bootstrap_servers=KAFKA_URI,
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
