from pydantic import BaseModel


class ResponseBody(BaseModel):
    """ https://msx.benzac.de/wiki/index.php?title=Responses """
    status: int = 200
    text: str = "OK"
    message: str | None = None
    data: dict = None


class Response(BaseModel):
    response: ResponseBody | BaseModel
