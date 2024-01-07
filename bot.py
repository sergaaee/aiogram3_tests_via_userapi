import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

from config import get_settings

TOKEN = get_settings().BOT_TOKEN

dp = Dispatcher()


@dp.message(Command(commands=['start']))
async def command_start_handler(message: Message) -> None:
    await message.answer("Hello, my dear!")
    await message.answer("Hello, my dear2!")
    await message.answer("Hello, my dear3!")
    await message.answer("Hello, my dear4!")
    await message.answer("Hello, my dear5!")
    await message.answer("Hello, my dear!6")


@dp.message(Command(commands=['stop', 'stopme']))
async def stop_handler(message: Message):
    await message.answer("Stopped1")
    await message.answer("Stopped2")
    await message.answer("Stopped3")
    await message.answer("Stopped13")
    await message.answer("Stopped25")
    await message.answer("Stopped37")


@dp.message(Command(commands=['help', 'helpme']))
async def help_handler(message: Message):
    await message.answer("Helped1")
    await message.answer("Helped1")
    await message.answer("Helped1")
    await message.answer("Helped1")
    await message.answer("Helped1")
    await message.answer("Helped112")
    await message.answer("Helped1123")
    await message.answer("Helpedasd1")
    await message.answer("Helped1asчd")
    await message.answer("Helped1asd")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
