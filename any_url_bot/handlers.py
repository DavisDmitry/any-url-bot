import aiogram
import aiogram.exceptions
import aiogram.types
import pydantic
from aiogram.utils import keyboard

from any_url_bot import url as _url

_START_TEXT = (
    "Send me an HTTPS URL and I'll reply with a message with a button to open it, "
    "just like a WebApp."
)
_INVALID_URL_TEXT = "The URL you sent is invalid."


router = aiogram.Router()


@router.message(commands="start", content_types=aiogram.types.ContentType.TEXT)
async def handle_start_cmd(msg: aiogram.types.Message):
    return msg.answer(_START_TEXT)


@router.message(content_types=aiogram.types.ContentType.TEXT)
async def handle_url(msg: aiogram.types.Message):
    url = _url.normalize_url(msg.text)  # type: ignore  # msg.text can't be None

    try:
        web_app = _url.WebAppInfo(url=url)
    except pydantic.ValidationError:
        return msg.answer(text=_INVALID_URL_TEXT)

    kb_builder = keyboard.InlineKeyboardBuilder()
    kb_builder.button(text=msg.text, web_app=web_app)
    await msg.answer(
        text=url, disable_web_page_preview=True, reply_markup=kb_builder.as_markup()
    )
