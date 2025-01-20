from enum import Enum

from pydantic import BaseModel, Field


class Template(BaseModel):
    type: str = "separate"
    layout: str = "0,0,1,1"


class ContentItem(BaseModel):
    """ https://msx.benzac.de/wiki/index.php?title=Content_Item_Object """
    label: str = ""
    title: str = ""
    titleHeader: str = ""
    titleFooter: str = ""
    action: str = ""
    icon: str = ""
    image: str = ""
    imageFiller: str = ""
    enumerate: bool = True
    alignment: str = "left"
    centration: str | None = None


class ContentRoot(BaseModel):
    """ https://msx.benzac.de/wiki/index.php?title=Content_Root_Object """

    class Type(str, Enum):
        list = "list"
        pages = "pages"

    type: str
    headline: str = ""
    template: Template = None
    items: list[ContentItem] = Field(default_factory=list)
