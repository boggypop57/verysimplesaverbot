import asyncio
from dotenv import load_dotenv 
import logging
import signal
import sys
from os import getenv
from typing import cast

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
if TOKEN is None:
    raise ValueError("BOT_TOKEN environment variable is not set")


dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if message.from_user is None:
        await message.answer("Hello, anonymous user!")
        return
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=cast(str,TOKEN), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot) 

def shutdown():
    print("Bot stopped gracefully")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda s, f: shutdown())
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
