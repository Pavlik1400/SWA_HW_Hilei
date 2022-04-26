from multiprocessing import Manager

from fastapi import FastAPI
from pydantic import BaseModel

from logs import LOGGER

controller = FastAPI()


class Message(BaseModel):
    uuid: str
    message: str


manager = Manager()
storage = manager.dict()


@controller.post("/")
def post_log(msg: Message):
    LOGGER.info(f"LOGGING: Add {msg.uuid}  ->  {msg.message}")
    storage[msg.uuid] = msg.message


@controller.get("/")
def get_log():
    LOGGER.info(f"LOGGING: get_logs()")
    return str(list(storage.values()))
