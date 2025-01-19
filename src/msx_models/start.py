from pydantic import BaseModel


class Start(BaseModel):
    name: str
    parameter: str = "menu:user::http://127.0.0.1:8000/msx/menu.json"
    version: str = "1.0.0"
