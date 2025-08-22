import logging
from os import getenv
from typing import cast

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

TOKEN = getenv("BOT_TOKEN")
assert TOKEN is not None, "BOT_TOKEN environment variable is not set"

WEB_SERVER_HOST = "0.0.0.0"
WEB_SERVER_PORT = 8000
WEBHOOK_HOST = "https://verysimplesaverbot-production.up.railway.app" 
WEBHOOK_PATH = f"/webhook/ffwo2o3im23424lmvss9902lmseklfmvm23z0z0z0m"  
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

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
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")

async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook set to: {WEBHOOK_URL}")

async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook()
    logging.info("Bot stopped. Webhook deleted.")

def main() -> None:
    bot = Bot(token=cast(str,TOKEN), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    app = web.Application()
    
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    logging.info("Starting web server...")
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
