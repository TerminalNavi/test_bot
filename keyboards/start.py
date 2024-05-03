'''Кнопки для команды /start'''
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb_next_btn = InlineKeyboardMarkup(inline_keyboard = [[
        InlineKeyboardButton(
            text = 'Вперёд',
            callback_data = 'next')]])

kb_back_btn = InlineKeyboardMarkup(inline_keyboard = [[
        InlineKeyboardButton(
            text = 'Назад',
            callback_data = 'back')]])
