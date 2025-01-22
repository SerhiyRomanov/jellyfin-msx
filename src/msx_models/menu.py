from enum import Enum
from typing import List

from pydantic import BaseModel

from msx_models.content import ContentRoot


class MenuItem(BaseModel):

    class Type(str, Enum):
        default = "default"
        separator = "separator"
        settings = "settings"

    label: str = ""
    type: str = Type.default.value
    data: str | ContentRoot = ""


class Menu(BaseModel):
    headline: str = "Menu"
    cache: bool = True
    menu: List[MenuItem]
