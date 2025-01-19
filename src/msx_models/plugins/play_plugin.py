from pydantic import BaseModel, computed_field, HttpUrl

from msx_models.plugins.base import BasePluginMixin
from msx_models.utils import add_query_params


class PlayPlugin(BasePluginMixin, BaseModel):
    """ https://msx.benzac.de/wiki/index.php?title=Play_Plugin """
    _plugin_url: HttpUrl = "https://msx.benzac.de/interaction/play.html"

    @computed_field
    def plugin_url(self) -> HttpUrl:
        return self.adjust_scheme(self._plugin_url)

    def build_action(self, video_url: str) -> str:
        return f"video:resolve:request:interaction:{video_url}@{str(self.plugin_url)}"
