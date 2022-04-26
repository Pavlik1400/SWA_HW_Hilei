from fastapi import FastAPI
from logs import LOGGER

controller = FastAPI()


@controller.get("/")
def get_messages():
    LOGGER.info("MESSAGES: get_messages()")
    return "message-service is not implemented yet"
