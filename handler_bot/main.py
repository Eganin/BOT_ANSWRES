import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from database import Sqliter
import common.text_for_bot as text
from utils import Utils

from utils.Builder import Bulder
import asyncio
import datetime

load_dotenv()  # load .env

TOKEN = str(os.getenv('TG_TOKEN'))  # api token from botfather

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
database: Sqliter.Sqliter = Sqliter.Sqliter("C:\\Users\\Eganin\\PycharmProjects\\BotAnswers\\database\\db.db")
utils: Utils.Utils = Utils.Utils()
builder_answer: Bulder = Bulder()


@dp.message_handler(commands=["start"])
async def start(message: types.Message) -> None:
    await message.answer(text.HELLO_BOT)
    await message.answer(text.START_ANSWERS)
    await message.answer(text.SAVE_TIME)


@dp.message_handler(lambda message: utils.is_time_input(message.text))
async def time(message: types.Message):
    builder_answer.setTime(message.text)
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
                           builder_answer.mentors,
                           builder_answer.time,
                           int(datetime.datetime.today().isoweekday()),
                           str(datetime.datetime.today().day))


async def check_time_send(time: int):
    while True:
        await asyncio.sleep(20)
        users: list = database.get_info_all_users()
        for i in users:

            print(i)
            now = datetime.datetime.now()
            if (str(now.hour) + ":" + str(now.minute)) == i[-3]:
                await bot.send_message(i[1], "Время опроса")
                await bot.send_message(i[1], text.NEW_START_ANSWERS)
                await bot.send_message(i[1], text.LEARN_TEXT)


async def check_day_send(time: int):
    while True:
        await asyncio.sleep(20)
        users: list = database.get_info_all_users()
        for i in users:
            print(i)
            weekday = datetime.datetime.today().isoweekday()
            if int(weekday) == int(i[-2]) and int(datetime.datetime.today().day) != int(i[-1]):
                score: int = database.statistic(i[1])
                if score > 12:
                    await bot.send_message(i[1], f"Результаты за неделю хорошие ,= {score}")


async def main():
    loop = asyncio.get_event_loop()
    task1 = loop.create_task(check_time_send(10))
    task2 = loop.create_task(check_day_send(10))
    await task1
    await task2

if __name__ == "__main__":
    main()

    executor.start_polling(dp, skip_updates=True)
