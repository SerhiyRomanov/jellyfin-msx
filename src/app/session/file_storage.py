import json
import os

from app.config import AppConfig
from app.session.base import BaseSessionStorage


# TODO: Convert to async implementation
class SessionFileStorage(BaseSessionStorage):
    folder: str

    def __init__(self):
        app_config = AppConfig()
        self.folder = app_config.session_file_storage_path

        if not os.path.exists(self.folder):
            os.mkdir(self.folder)

    def _get_file_name(self, key):
        return f"{self.folder}{key}.json"

    def _load_session(self, key: str) -> dict:
        # TODO: Implement expiration check using app_config.session_max_age
        fn = self._get_file_name(key)
        if os.path.exists(fn):
            with open(fn, "r") as f:
                return json.loads(f.read())
        return dict()

    def _save_session(self, key: str, data: dict) -> None:
        with open(self._get_file_name(key), "w") as f:
            f.write(json.dumps(data))

    def get(self, session_key: str, key: str) -> str | None:
        values = self._load_session(session_key)
        return values.get(key)

    def set(self, session_key: str, key: str, value: str) -> None:
        values = self._load_session(session_key)
        values[key] = value
        self._save_session(session_key, values)
