from pydantic import BaseModel, computed_field, HttpUrl

from msx_models.plugins.base import BasePluginMixin
from msx_models.utils import add_query_params


class InputPluginAction(BaseModel):
    """ https://msx.benzac.de/wiki/index.php?title=Input_Plugin, see Usage section """
    url: str
    # input: str = ""
    type: str = "default"
    default_lang: str = ""
    headline: str = ""
    background: str = ""
    extension: str = ""
    hint: str = ""
    placeholder: str = ""
    limit: str = ""
    init_input: str = ""

    def build_action(self) -> str:
        url = self.url
        url = add_query_params(url, dict(input="{INPUT}", credentials=1))

        action_param_values = (
            url,
            self.type, self.default_lang, self.headline, self.background, self.extension,
            self.hint, self.limit, self.placeholder, self.limit, self.init_input
        )

        params_prepared = "|".join(action_param_values)

        return f"content:request:interaction:{params_prepared}"


class InputPlugin(BasePluginMixin, BaseModel):
    """ https://msx.benzac.de/wiki/index.php?title=Input_Plugin """
    _plugin_url: HttpUrl = "https://msx.benzac.de/interaction/input.html"

    @computed_field
    def plugin_url(self) -> HttpUrl:
        return self.adjust_scheme(self._plugin_url)

    def build_action(self, action: InputPluginAction) -> str:
        action_string = action.build_action()
        return f"{action_string}@{str(self.plugin_url)}"
