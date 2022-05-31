from fastapi import FastAPI
from pydantic import BaseModel

from hazelcast_wrapper import HazelcastWrapper
from logs import LOGGER
from constants import HAZELCAST_MAP_KEY, DEFAULT_HAZELCAST_MAP_NAME
from utils import get_or_set_default_consul
import consul

controller = FastAPI()


class Message(BaseModel):
    uuid: str
    message: str


c = consul.Consul()
logging_map_name = get_or_set_default_consul(c, key=HAZELCAST_MAP_KEY, default=DEFAULT_HAZELCAST_MAP_NAME)
hz_instance = HazelcastWrapper.newHazelCastInstance()
log_messages = hz_instance.get_map(logging_map_name)


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
