import httpx

from .utils import add_query_params


class AppConfig:
    # Client meta info
    client: str = "Python JellyfinAsyncClient"
    device: str = ""
    device_id: str = ""
    version: str = "0.0.1"
    user_agent: str = "Python JellyfinAsyncClient/0.0.1"


class AuthConfig:
    # Auth related
    server_url: str = ""
    access_token: str = ""
    user_id = str = ""


class JellyfinAsyncClient:
    app_config: AppConfig
    auth_config: AuthConfig

    _http_client: httpx.AsyncClient | None

    def __init__(self, config: AppConfig = None):
        self._http_client = None
        self.app_config = config or AppConfig()
        self.auth_config = config or AuthConfig()

    async def __aenter__(self):
        self._http_client = httpx.AsyncClient()
        return self

    async def __aexit__(self, *args, **kwargs):
        if self._http_client is not None:
            await self._http_client.aclose()

    def _get_authenication_header(self):
        params = {}
        params.update({
            "Client": self.app_config.client,
            "Device": self.app_config.device,
            "DeviceId": self.app_config.device_id,
            "Version": self.app_config.version
        })

        if self.auth_config.access_token:
            params["Token"] = self.auth_config.access_token

        param_line = ",".join(f'{k}="{v}"' for k, v in params.items())
        return f"MediaBrowser {param_line}"

    def _get_default_headers(self, content_type="application/json"):
        app_name = f"{self.app_config.client}/{self.app_config.version}"
        return {
            "Accept": "application/json",
            "Content-type": content_type,
            "X-Application": app_name,
            "Accept-Charset": "UTF-8,*",
            "Accept-encoding": "gzip",
            "User-Agent": self.app_config.user_agent,
            "Authorization": self._get_authenication_header()
        }

    def _align_protocol(self, server_url):
        if not server_url.startswith("http"):
            server_url = "https://" + server_url
        return server_url

    def _create_full_url(self, server_url: str, endpoint) -> str:
        """ return URL without trailing slash """
        # Add protocol (HTTPS by default)
        server_url = self._align_protocol(server_url)

        # Ensure not trailing slash in server_url
        server_url = server_url.rstrip("/")

        # Ensure that endpoint starts with slash
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint

        return server_url + endpoint

    async def request(self, method: str, endpoint: str, **kwargs) -> dict:
        if self._http_client:
            close_after_request = False
            client = self._http_client
        else:
            close_after_request = True
            client = httpx.AsyncClient()

        client.headers = self._get_default_headers()

        try:
            response = await client.request(
                method=method,
                url=self._create_full_url(self.auth_config.server_url, endpoint),
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        finally:
            if close_after_request:
                await client.aclose()

    def create_videos_stream_url(self, item_id: str, container: str = None, params: dict = None) -> str:
        url = self._create_full_url(self.auth_config.server_url, f"/Videos/{item_id}/stream")
        if container:
            url += f".{container}"

        if params is not None:
            url = add_query_params(url, params)
        return url

    def create_items_image_url(self, item_id: str, image_type: str, params: dict = None) -> str:
        url = self._create_full_url(self.auth_config.server_url, f"/Items/{item_id}/Images/{image_type}")
        if params is not None:
            url = add_query_params(url, params)
        return url
