from typing import Literal

import pydantic
from aiogram.utils import token

from any_url_bot import url

LoggingLevel = Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]


class Config(pydantic.BaseSettings):
    # pylint: disable=R0903
    log_level: LoggingLevel = pydantic.Field("INFO", env="LOG_LEVEL")
    bot_token: str = pydantic.Field(..., env="BOT_TOKEN")
    webhook_url: url.HttpsUrl = pydantic.Field(..., env="WEBHOOK_URL")

    @pydantic.validator("log_level", pre=True)
    @classmethod
    def validate_log_level(cls, log_level: str) -> str:
        return log_level.upper()

    @pydantic.validator("bot_token")
    @classmethod
    def validate_bot_token(cls, bot_token: str) -> str:
        token.validate_token(bot_token)
        return bot_token
