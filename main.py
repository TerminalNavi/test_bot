import requests
from db import *
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters.command import Command



bot_token = open('config.txt').readline()
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(bot_token)
# Диспетчер
dp = Dispatcher()
router = Router()

# Запуск процесса поллинга новых апдейтов
# async def main():
#     await router.start_polling(bot)



@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await bot.set_my_commands([
        types.BotCommand(command='start', description='Запуск бота'),
        types.BotCommand(command='help', description='Справка'),
        types.BotCommand(command='delete', description='Отчислиться')
    ])

    inline_markup = types.InlineKeyboardMarkup(inline_keyboard = [
        [types.InlineKeyboardButton(text = 'Вперёд', callback_data = 'next')]
    ])

    await message.answer("Страница 1", reply_markup=inline_markup)

@router.callback_query(F.data == 'next')
async def next_handler(callback_query: types.CallbackQuery):
    inline_markup = types.InlineKeyboardMarkup(inline_keyboard = [
        [types.InlineKeyboardButton(text = 'Назад', callback_data = 'back')]
    ])
    await callback_query.message.delete()
    await callback_query.message.answer(
        text='Страница 2',
        reply_markup=inline_markup
    )

@router.callback_query(F.data == 'back')
async def back_handler(callback_query: types.CallbackQuery):
    inline_markup = types.InlineKeyboardMarkup(inline_keyboard = [
        [types.InlineKeyboardButton(text = 'Вперёд', callback_data = 'next')]
    ])
    await callback_query.message.delete()
    await callback_query.message.answer(
        text='Страница 1',
        reply_markup=inline_markup
    )

async def main():
    await dp.start_polling(bot)

dp.include_router(router)


if __name__ == "__main__":
    asyncio.run(main())
