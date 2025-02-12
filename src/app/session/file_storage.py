import json
import os

from anyio import Path

from app.config import AppConfig
from app.session.base import BaseSessionStorage


class SessionFileStorage(BaseSessionStorage):
    folder: str

    def __init__(self):
        app_config = AppConfig()
        self.folder = app_config.session_file_storage_path

        if not os.path.exists(self.folder):
            os.mkdir(self.folder)

    def _get_session_path_object(self, key) -> Path:
        return Path(self.folder) / f"{key}.json"

    async def _load_session(self, key: str) -> dict:
        # TODO: Implement expiration check using app_config.session_max_age
        session_file = self._get_session_path_object(key)
        if await session_file.exists():
            return json.loads(await session_file.read_bytes())
        return dict()

    async def _save_session(self, key: str, data: dict) -> None:
        session_file = self._get_session_path_object(key)
        await session_file.write_text(json.dumps(data))

    async def get(self, session_key: str, key: str) -> str | None:
        values = await self._load_session(session_key)
        return values.get(key)

    async def set(self, session_key: str, key: str, value: str) -> None:
        values = await self._load_session(session_key)
        values[key] = value
        await self._save_session(session_key, values)

    async def clear(self, session_key: str) -> None:
        session_file = self._get_session_path_object(session_key)
        await session_file.unlink()
