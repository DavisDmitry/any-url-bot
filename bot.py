import asyncio
import logging
import os

import aiogram
import aiogram.exceptions
import aiogram.types

logging.basicConfig(level="DEBUG")


_BOT = aiogram.Bot(os.environ["BOT_TOKEN"])
_DISPATCHER = aiogram.Dispatcher()
_START_TEXT = (
    "Send me an HTTPS URL and I'll reply with a message with a button to open it, "
    "just like a WebApp."
)
_INVALID_URL_TEXT = "The URL you sent is invalid."


@_DISPATCHER.message(commands="start", content_types=aiogram.types.ContentType.TEXT)
async def handle_start_cmd(msg: aiogram.types.Message):
    return msg.answer(_START_TEXT)


@_DISPATCHER.message(content_types=aiogram.types.ContentType.TEXT)
async def handle_another_msgs(msg: aiogram.types.Message):
    url: str = msg.text  # type: ignore # cause only text messages handled
    if url.startswith("http://"):
        url = url.replace("http://", "https://", 1)
    if not url.startswith("https://"):
        url = f"https://{url}"
    try:
        await msg.answer(
            url,
            disable_web_page_preview=True,
            reply_markup=aiogram.types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        aiogram.types.InlineKeyboardButton(
                            text=url.replace("https://", "", 1),
                            web_app=aiogram.types.WebAppInfo(url=url),
                        )
                    ]
                ]
            ),
        )
    except aiogram.exceptions.TelegramBadRequest:
        return msg.answer(_INVALID_URL_TEXT)


if __name__ == "__main__":
    asyncio.run(_DISPATCHER.start_polling(_BOT, allowed_updates=["message"]))
