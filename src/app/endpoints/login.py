from typing import Annotated

from fastapi import APIRouter, Request, Body
from pydantic import BaseModel

from app.dependencies import UserSessionDep
from app.session.user_session import UserSession, JellyfinAuthData
from jellyfin_api.api import JellyfinAsyncClient
from msx_models.content import ContentRoot, ContentPage, ContentItem
from msx_models.plugins.input_plugin import InputPluginAction, InputPlugin
from msx_models.response import Response, ResponseBody
from msx_models.utils import add_query_params

from app.endpoints.utils import build_msx_uri


router = APIRouter()


class Credentials(BaseModel):
    server_url: str | None = ""
    username: str | None = ""
    password: str | None = ""


@router.get("/login.json")
def login_json(
        request: Request,
        step: str = "start", input: str = "",
        server_url: str | None = "", username: str | None = "", password: str | None = ""
):
    login_endpoint = build_msx_uri(str(request.url_for("login_json")))
    input_plugin = InputPlugin()

    credentials = Credentials(server_url=server_url, username=username, password=password)

    match step:
        case "start":
            enter_server_action = InputPluginAction(
                url=add_query_params(login_endpoint, dict(step="store_server_url", **credentials.model_dump())),
                headline="Enter the server URL",
                hint="Enter the server URL",
            )
            return Response(
                response=ResponseBody(data=dict(action=input_plugin.build_action(enter_server_action)))
            )
        case "store_server_url":
            credentials.server_url = input
            enter_username_action = InputPluginAction(
                url=add_query_params(login_endpoint, dict(step="store_username", **credentials.model_dump())),
                headline="Enter the  username",
                hint="Enter the username",
            )
            return Response(
                response=ResponseBody(data=dict(action=input_plugin.build_action(enter_username_action)))
            )

        case "store_username":
            credentials.username = input
            enter_password_action = InputPluginAction(
                url=add_query_params(login_endpoint, dict(step="store_password", **credentials.model_dump())),
                headline="Enter the password",
                hint="Enter the password"
            )

            return Response(
                response=ResponseBody(data=dict(action=input_plugin.build_action(enter_password_action)))
            )

        case "store_password":
            credentials.password = input

            login_service = build_msx_uri(str(request.url_for("login")))
            return Response(
                response=ResponseBody(
                    data=dict(
                        action=f"execute:accurate:{login_service}",
                        data=credentials.model_dump()
                    )
                )
            )


@router.post("/login")
async def login(id: str, data: Annotated[Credentials, Body(embed=True)]):
    jellyfin = JellyfinAsyncClient()
    jellyfin.app_config.device = "Jellyfin-MSX"
    jellyfin.app_config.device_id = id
    jellyfin.auth_config.server_url = data.server_url

    resp = await jellyfin.request(
        "POST", "/Users/AuthenticateByName",
        json=dict(Username=data.username, Pw=data.password)
    )

    if resp:
        session = UserSession(id)
        await session.store_auth_data(
            JellyfinAuthData(
                server_url=data.server_url,
                access_token=resp["AccessToken"],
                user_id=resp["User"]["Id"]
            ))

        return Response(
            response=ResponseBody(data=dict(action="[info:Successfully logged in|reload]"))
        )

    return Response(
        response=ResponseBody(data=dict(action="error:Unable to login"))
    )


@router.get("/server_info.json")
async def server_info_json(request: Request, user_session: UserSessionDep):
    auth_data = await user_session.get_auth_data()
    logout_url = build_msx_uri(str(request.url_for("logout")))

    return ContentRoot(
        type=ContentRoot.Type.pages.value,
        pages=[ContentPage(
            items=[
                ContentItem(
                    layout="0,0,12,2",
                    text=f"Server URL: {auth_data.server_url}",
                    enumerate=False,
                ),
                ContentItem(
                    type=ContentItem.Type.default,
                    layout="0,3,12,1",
                    label="Logout",
                    enumerate=False,
                    action=f"execute:accurate:{logout_url}",
                )
            ]
        )]
    )


@router.post("/logout")
async def logout(user_session: UserSessionDep):
    await user_session.clear()
    return Response(
        response=ResponseBody(
            data=dict(
                action="[info:Successfully logged out|reload]",
            )
        )
    )
