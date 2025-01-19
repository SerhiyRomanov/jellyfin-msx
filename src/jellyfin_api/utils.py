from urllib.parse import urlparse, urlunparse, parse_qs, urlencode, unquote


def add_query_params(url: str, query_params: dict) -> str:
    parsed = urlparse(url)
    new_query_params = parse_qs(parsed.query)
    new_query_params.update(query_params)
    qs_str = unquote(urlencode(new_query_params, doseq=True))
    return urlunparse(
        (parsed.scheme, parsed.netloc, parsed.path, parsed.params, qs_str, parsed.fragment)
    )
