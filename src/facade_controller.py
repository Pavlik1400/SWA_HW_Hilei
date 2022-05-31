from fastapi import FastAPI, Request, Response, status as fa_status

from facade_service import FacadeService
from logs import LOGGER

controller = FastAPI()
facade = FacadeService()


@controller.post("/")
async def post_message(message: Request):
    body = await message.body()
    facade.add_message(body.decode())


@controller.get("/")
async def get_message(response: Response):
    try:
        status, resp = facade.get_messages()
    except Exception as exc:
        response.status_code = fa_status.HTTP_500_INTERNAL_SERVER_ERROR
        error_messae = f"Error happened in internal communication between services: {exc}"
        LOGGER.error(error_messae)
        return error_messae

    if status != fa_status.HTTP_200_OK:
        LOGGER.warning(resp)
        response.status_code = status
        return resp

    return resp
