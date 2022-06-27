import string
from typing import Literal

import pydantic
from aiogram.utils import token

from any_url_bot import url

_WEBHOOK_SECRET_ALPHABET = "".join((string.ascii_letters, string.digits, "-_"))


LoggingLevel = Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]


class Config(pydantic.BaseSettings):
    # pylint: disable=R0903
    log_level: LoggingLevel = pydantic.Field("INFO", env="LOG_LEVEL")
    bot_token: str = pydantic.Field(..., env="BOT_TOKEN")
    webhook_url: url.HttpsUrl = pydantic.Field(..., env="WEBHOOK_URL")
    webhook_secret: str | None = pydantic.Field(
        None, min_length=1, max_length=256, env="WEBHOOK_SECRET"
    )

    @pydantic.validator("log_level", pre=True)
    @classmethod
    def validate_log_level(cls, log_level: str) -> str:
        return log_level.upper()

    @pydantic.validator("bot_token")
    @classmethod
    def validate_bot_token(cls, bot_token: str) -> str:
        token.validate_token(bot_token)
        return bot_token

    @pydantic.validator("webhook_secret")
    @classmethod
    def validate_webhook_secret(cls, webhook_secret: str | None) -> str | None:
        if webhook_secret is None:
            return webhook_secret
        for char in webhook_secret:
            if char not in _WEBHOOK_SECRET_ALPHABET:
                raise ValueError
        return webhook_secret
