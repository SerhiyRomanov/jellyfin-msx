from pydantic import HttpUrl
from msx_models.config import Config


class BasePluginMixin:
    def adjust_scheme(self, url: HttpUrl | str) -> HttpUrl:
        config = Config()

        if config.use_https:
            url = str(url).replace("http://", "https://")
        else:
            url = str(url).replace("https://", "http://")

        return HttpUrl(url)
