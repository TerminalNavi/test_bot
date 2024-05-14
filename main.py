'''Несколько жизненно необходимых модулей'''
import asyncio
import logging
# from datetime import datetime
from aiogram import Bot, Dispatcher
from handlers import include_routers

logging.basicConfig(level=logging.INFO)

bot_token = open('config.txt', encoding='UTF-8').readline()
bot = Bot(bot_token)

dp = Dispatcher()




async def main():
    '''Функция для запуска бота'''
    include_routers(dp)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
