import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from database import Sqliter
import common.text_for_bot as text
from utils import Utils
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from utils.Builder import Bulder

load_dotenv()

TOKEN: str = str(os.getenv("TG_TOKEN"))

logging.basicConfig(level=logging.INFO)
bot: Bot = Bot(token=TOKEN)
dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
database: Sqliter.Sqliter = Sqliter.Sqliter("db")
utils: Utils.Utils = Utils.Utils()
builder_answer: Bulder = Bulder()


@dp.message_handler(commands=["start"])
async def start(message: types.Message) -> None:
    await message.answer(text.HELLO_BOT)

    await message.answer(text.START_ANSWERS)


@dp.message_handler(lambda message: utils.is_time_input(message.text))
async def time(message: types.Message):
    builder_answer.setTime(str(message))
    await message.answer("Время сохранено")


@dp.message_handler(commands=["start_polling"])
async def start_polling(message: types.Message):
    await message.answer(text.NEW_START_ANSWERS)
    await message.answer(text.LEARN_TEXT)


@dp.message_handler(commands=["learn"])
async def settings(message: types.Message):
    answer = str(message.text).split(" ")[1]
    builder_answer.setLearn(answer)
    await message.answer(text.SLEEP_TEXT)


@dp.message_handler(commands=["sleep"])
async def settings(message: types.Message):
    answer = str(message.text).split(" ")[1]
    builder_answer.setSleep(answer)
    await message.answer(text.SPORT_TEXT)


@dp.message_handler(commands=["sport"])
async def settings(message: types.Message):
    answer = str(message.text).split(" ")[1]
    builder_answer.setSport(answer)
    await message.answer(text.MENTORS_TEXT)


@dp.message_handler(commands=["thanks"])
async def settings(message: types.Message):
    answer = str(message.text).split(" ")[1]
    builder_answer.setMentors(answer)
    await message.answer(text.END_ANSWERS)
    database.add_user_info(message.from_user.id,
                           builder_answer.learn,
                           builder_answer.sleep,
                           builder_answer.sport,
                           builder_answer.mentors)


if __name__ == "__main__":
    executor.start_polling(dp,
                           skip_updates=True)
