from telegram import Bot
from telegram.error import TelegramError
from telegram.parsemode import ParseMode

from config.settings import settings

token = settings.TELEGRAM_TOKEN

bot = Bot(token=token)

chat_id = settings.TELEGRAM_CHAT_ID


def send_message(text: str) -> None:
    try:
        bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.MARKDOWN_V2)
    except TelegramError as e:
        print(e)
