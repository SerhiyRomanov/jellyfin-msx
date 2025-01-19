from starlette.datastructures import URL

from app.config import AppConfig


def build_msx_uri(url: str) -> str:
    config = AppConfig()

    parsed_config_url = URL(str(config.msx_url))
    parsed_target = URL(url)

    parsed_target.replace(
        scheme=parsed_config_url.scheme,
        netloc=parsed_config_url.netloc,
        port=parsed_config_url.port
    )

    return str(parsed_target)
