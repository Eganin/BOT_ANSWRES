import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from database import Sqliter
import common.text_for_bot as text

load_dotenv()

TOKEN: str = str(os.getenv("TG_TOKEN"))

logging.basicConfig(level=logging.INFO)
bot: Bot = Bot(token=TOKEN)
dp: Dispatcher = Dispatcher(bot)
database: Sqliter = Sqliter.Sqliter("db")


@dp.message_handler(commands=["start"])
async def start(message: types.Message) -> None:
    await message.answer(text.HELLO_BOT)
    await message.answer(text.HELLO_BOT)

@dp.message_handler(commands=["settings"])


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
