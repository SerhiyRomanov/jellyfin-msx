from typing import Annotated

from fastapi import Depends

from app.session.user_session import UserSession
from jellyfin_api.api import JellyfinAsyncClient


def get_user_session(id: str) -> UserSession:
    session = UserSession(id)
    return session


UserSessionDep = Annotated[UserSession, Depends(get_user_session)]


def get_jellyfin_client(session: UserSessionDep) -> JellyfinAsyncClient:
    if session.is_authenticated():
        auth_data = session.get_auth_data()
        jellyfin = JellyfinAsyncClient()
        jellyfin.app_config.device = "Jellyfin-MSX"
        jellyfin.app_config.device_id = session.session_key
        jellyfin.auth_config.server_url = auth_data.server_url
        jellyfin.auth_config.access_token = auth_data.access_token
        jellyfin.auth_config.user_id = auth_data.user_id
        return jellyfin


JellyFinDep = Annotated[JellyfinAsyncClient, Depends(get_jellyfin_client)]
