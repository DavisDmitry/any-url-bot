import logging

import aiogram
import aiogram.exceptions
import aiogram.types
from aiogram.dispatcher.webhook import aiohttp_server  # type: ignore  # 🙁
from aiohttp import web

from any_url_bot import config as _config
from any_url_bot import handlers


async def on_startup(
    bot: aiogram.Bot, dispatcher: aiogram.Dispatcher, webhook_url: str
):
    await bot.set_webhook(
        webhook_url, allowed_updates=dispatcher.resolve_used_update_types()
    )


def main():
    config = _config.Config()

    logging.basicConfig(level=config.log_level)

    bot = aiogram.Bot(config.bot_token, parse_mode="html")
    disp = aiogram.Dispatcher(disable_fsm=True)
    disp.startup.register(on_startup)
    disp.include_router(handlers.router)

    logging.getLogger("aiohttp.access").setLevel(logging.WARNING)
    app = web.Application()
    path = "/" if config.webhook_url.path is None else config.webhook_url.path
    aiohttp_server.SimpleRequestHandler(disp, bot, handle_in_background=False).register(
        app, path=path
    )
    aiohttp_server.setup_application(app, disp, bot=bot, webhook_url=config.webhook_url)
    web.run_app(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
