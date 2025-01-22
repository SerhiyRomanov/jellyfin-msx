from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class Template(BaseModel):
    type: str = "separate"
    layout: str = "0,0,1,1"


class ContentItem(BaseModel):
    """ https://msx.benzac.de/wiki/index.php?title=Content_Item_Object """

    class Type(str, Enum):
        default = "default"
        teaser = "teaser"
        button = "button"
        separate = "separate"
        space = "space"
        control = "control"

    type: str = Type.default.value
    layout: str = None
    enable: bool = True
    label: str = ""
    title: str = ""
    titleHeader: str = ""
    titleFooter: str = ""
    action: str = ""
    icon: str = ""
    image: str = ""
    imageFiller: str = ""
    enumerate: bool = True
    text: str = None
    alignment: str = "left"
    centration: str | None = None


class ContentPage(BaseModel):
    """ https://msx.benzac.de/wiki/index.php?title=Content_Page_Object """
    items: List[ContentItem] = Field(default_factory=list)


class ContentRoot(BaseModel):
    """ https://msx.benzac.de/wiki/index.php?title=Content_Root_Object """

    class Type(str, Enum):
        list = "list"
        pages = "pages"

    type: str
    headline: str = ""
    template: Template = None
    pages: list[ContentPage] = Field(default=None)
    items: list[ContentItem] = Field(default=None)
