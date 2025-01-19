from fastapi import APIRouter, Request

from app.dependencies import UserSessionDep
from app.endpoints.utils import build_msx_uri
from msx_models.content import ContentRoot, ContentItem, Template
from msx_models.menu import Menu, MenuItem
from msx_models.utils import expect_keywords

router = APIRouter()


@router.get("/menu.json")
def menu_json(request: Request, user_session: UserSessionDep):
    if user_session.is_authenticated():
        home_page_url = build_msx_uri(str(request.url_for("home_json")))
        return Menu(
            menu=[
                MenuItem(
                    label="Home",
                    data=f"{expect_keywords(home_page_url)}"
                ),
                MenuItem(
                    label="Recently watched (TODO)"
                ),
            ]
        )
    else:
        # Non authorised, show Login screen
        login_endpoint = build_msx_uri(str(request.url_for("login_json")))
        return Menu(
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
