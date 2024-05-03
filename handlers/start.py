'''Модуль обработки запросов команды /start'''
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, BotCommand, CallbackQuery
from keyboards.start import *


router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    '''Метод для инициализации списка команд'''
    await message.bot.set_my_commands([
        BotCommand(command='start', description='Запуск бота'),
        BotCommand(command='help', description='Справка'),
        BotCommand(command='delete', description='Отчислиться')])
    await message.answer("Страница 1", reply_markup=kb_next_btn)

@router.callback_query(F.data == 'next')
async def next_handler(callback_query: CallbackQuery):
    '''Метод для создания кнопки вперёд для команды /start'''
    await callback_query.message.edit_text(
        text='Страница 2', reply_markup=kb_back_btn)

@router.callback_query(F.data == 'back')
async def back_handler(callback_query: CallbackQuery):
    '''Метод для создания кнопки назад для команды /start'''
    await callback_query.message.delete()
    await callback_query.message.answer(
        text='Страница 1', reply_markup=kb_next_btn)
