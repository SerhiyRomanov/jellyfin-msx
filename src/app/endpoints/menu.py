from fastapi import APIRouter, Request

from app.dependencies import UserSessionDep
from app.endpoints.utils import build_msx_uri
from msx_models.content import ContentRoot, ContentItem, Template
from msx_models.menu import Menu, MenuItem

router = APIRouter()


@router.get("/menu.json")
async def menu_json(request: Request, user_session: UserSessionDep):
    if await user_session.is_authenticated():
        return Menu(
            cache=False,
            menu=[
                MenuItem(
                    label="Home",
                    data=build_msx_uri(str(request.url_for("home_json"))),
                ),
                MenuItem(
                    label="Recently watched (TODO)"
                ),
                MenuItem(
                    type=MenuItem.Type.separator.value,
                ),
                MenuItem(
                    label="Server info",
                    data=build_msx_uri(str(request.url_for("server_info_json"))),
                ),
            ]
        )
    else:
        # Non authorised, show Login screen
        login_endpoint = build_msx_uri(str(request.url_for("login_json")))
        return Menu(
            cache=False,
            menu=[
                MenuItem(
                    label="Login",
                    data=ContentRoot(
                        headline="Login to Jellyfin server using username and password",
                        type=ContentRoot.Type.list,
                        template=Template(layout="0,0,12,3"),
                        items=[
                            ContentItem(
                                label="Login on Jellyfin server",
                                action=f"execute:fetch:{login_endpoint}",
                                enumerate=False,
                                alignment="justify|text-justify",
                                centration="text"
                            )
                        ]
                    )
                )
            ]
        )
