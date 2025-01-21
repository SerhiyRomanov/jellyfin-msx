import json

from pydantic import BaseModel

from .file_storage import SessionFileStorage


class JellyfinAuthData(BaseModel):
    user_id: str
    server_url: str
    access_token: str


class UserSession:
    key_jellyfin_auth_data = "jellyfin_auth_data"

    def __init__(self, session_key: str):
        self._session_key = session_key
        self.storage = SessionFileStorage()

    @property
    def session_key(self) -> str:
        return self._session_key

    async def get_key(self, key: str, default=None) -> str | None:
        return await self.storage.get(self._session_key, key) or default

    async def set_key(self, key: str, value: str) -> None:
        return await self.storage.set(self._session_key, key, value)

    async def clear(self):
        await self.storage.clear(self._session_key)

    # Convenient methods
    async def store_auth_data(self, data: JellyfinAuthData) -> None:
        await self.set_key(self.key_jellyfin_auth_data, data.model_dump_json())

    async def get_auth_data(self) -> JellyfinAuthData | None:
        data = await self.get_key(self.key_jellyfin_auth_data)
        if data:
            parsed = json.loads(data)
            return JellyfinAuthData(**parsed)
        return None

    async def is_authenticated(self) -> bool:
        return await self.get_key(self.key_jellyfin_auth_data) is not None
