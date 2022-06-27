import aiogram.types
import pydantic


def normalize_url(url: str) -> str:
    if url.startswith("http://"):
        url = url.replace("http://", "https://", 1)
    if not url.startswith("https://"):
        url = f"https://{url}"
    return url


class HttpsUrl(pydantic.AnyUrl):
    # pylint: disable=E1101,R0903
    allowed_schemes = {"https"}
    tld_required = True


class WebAppInfo(aiogram.types.WebAppInfo):
    # pylint: disable=E1101,R0903
    url: HttpsUrl
