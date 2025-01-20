from abc import ABC


class BaseSessionStorage(ABC):

    def get(self, session_key: str, key: str) -> str | None:
        raise NotImplementedError

    def set(self, session_key, key: str, value: str) -> None:
        raise NotImplementedError

    def clear(self, session_key: str) -> None:
        raise NotImplementedError
