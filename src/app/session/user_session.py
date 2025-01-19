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

    def get_key(self, key: str, default=None) -> str | None:
        return self.storage.get(self._session_key, key) or default

    def set_key(self, key: str, value: str) -> None:
        return self.storage.set(self._session_key, key, value)

    def delete(self):
        raise NotImplementedError

    # Convenient methods
    def store_auth_data(self, data: JellyfinAuthData) -> None:
        self.set_key(self.key_jellyfin_auth_data, data.model_dump_json())

    def get_auth_data(self) -> JellyfinAuthData | None:
        data = self.get_key(self.key_jellyfin_auth_data)
        if data:
            parsed = json.loads(data)
            return JellyfinAuthData(**parsed)
        return None

    def is_authenticated(self) -> bool:
        return self.get_key(self.key_jellyfin_auth_data) is not None
