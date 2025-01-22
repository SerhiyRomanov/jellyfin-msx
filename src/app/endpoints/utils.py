from starlette.datastructures import URL

from app.config import AppConfig
from msx_models.utils import expect_keywords


def build_msx_uri(url: str, expected_keywords: list = None) -> str:
    config = AppConfig()

    parsed_config_url = URL(str(config.msx_url))
    parsed_target = URL(url)

    # Ensure correct host
    parsed_target = parsed_target.replace(
        scheme=parsed_config_url.scheme,
        netloc=parsed_config_url.netloc,
        port=parsed_config_url.port
    )
    result_url = str(parsed_target)

    # For our application we always expect at least ID
    expected_keywords = expected_keywords or []
    expected_keywords.append("ID")
    result_url = expect_keywords(result_url, expected_keywords)

    return result_url
