from pydantic import Field, AnyHttpUrl, computed_field, HttpUrl
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    msx_url: HttpUrl = Field("http://127.0.0.1:8000")

    @computed_field
    def use_https(self) -> bool:
        return self.msx_url.scheme == "https"
