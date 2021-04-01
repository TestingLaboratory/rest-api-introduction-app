from pydantic import BaseModel


class Pong(BaseModel):
    request_body: str
