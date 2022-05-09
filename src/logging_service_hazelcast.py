from fastapi import FastAPI
from pydantic import BaseModel

from hazelcast_wrapper import HazelcastWrapper
from logs import LOGGER

controller = FastAPI()


class Message(BaseModel):
    uuid: str
    message: str


hz_instance = HazelcastWrapper.newHazelCastInstance()
log_messages = hz_instance.get_map("logging_map")


@controller.post("/")
def post_log(msg: Message):
    LOGGER.info(f"LOGGING: Add {msg.uuid}  ->  {msg.message}")
    log_messages.put(msg.uuid, msg.message)


@controller.get("/")
def get_log():
    LOGGER.info(f"LOGGING: get_logs()")
    v = str(list(log_messages.values().result()))
    LOGGER.debug(v)
    return v
