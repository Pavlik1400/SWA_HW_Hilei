from fastapi import FastAPI, Request, Response, status as fa_status

from facade_service import FacadeService

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
        return f"Error happened in internal communication between services: {exc}"

    if status != fa_status.HTTP_200_OK:
        response.status_code = status
        return resp

    return resp
