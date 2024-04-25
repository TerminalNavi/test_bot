import asyncio
import logging
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import Message, BotCommand, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup



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

class Anketa(StatesGroup):
    name = State()
    age = State()
    gender = State()

@router.message(Command("anketa"))
async def anketa_handler(message: Message, state:FSMContext):
    await state.set_state(Anketa.name)
    markup = InlineKeyboardMarkup(inline_keyboard = [[
        InlineKeyboardButton(text = 'Отмена', callback_data = 'cancel_anketa')]])
    await message.answer("Введите Ваше имя", reply_markup=markup)

@router.callback_query(F.data == 'cancel_anketa')
async def cancel_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.answer('Регистрация отменена')

@router.message(Anketa.name)
async def set_name_by_anketa_handler(message: Message, state:FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Anketa.age)
    markup = InlineKeyboardMarkup(inline_keyboard = [[
        InlineKeyboardButton(text = 'Назад', callback_data = 'set_name_anketa'),
        InlineKeyboardButton(text = 'Отмена', callback_data = 'cancel_anketa')]])
    await message.answer("Введите Ваш возраст", reply_markup=markup)

@router.callback_query(F.data == 'set_name_anketa')
async def set_name_anketa_handler(callback_query: CallbackQuery, state: FSMContext):
    await anketa_handler(callback_query.message, state)

@router.message(Anketa.age)
async def set_age_by_anketa_handler(message: Message, state:FSMContext):
    try:
        await state.update_data(age = int(message.text))
    except ValueError:
        await message.answer("Вы неверно ввели возраст")
        markup = InlineKeyboardMarkup(inline_keyboard = [[
            InlineKeyboardButton(text = 'Назад', callback_data = 'set_name_anketa'),
            InlineKeyboardButton(text = 'Отмена', callback_data = 'cancel_anketa')]])
        await message.answer("Введите Ваш возраст", reply_markup=markup)
        return
    
    await state.set_state(Anketa.gender)
    markup = InlineKeyboardMarkup(inline_keyboard = [[
        InlineKeyboardButton(text = 'Мужской', callback_data = 'male'),
        InlineKeyboardButton(text = 'Женский', callback_data = 'female')],
        [InlineKeyboardButton(text = 'Назад', callback_data = 'set_age_anketa'),
        InlineKeyboardButton(text = 'Отмена', callback_data = 'cancel_anketa')]])
    await message.answer("Введите Ваш пол", reply_markup=markup)

@router.callback_query(F.data == 'set_age_anketa')
async def set_age_anketa_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Anketa.age)
    markup = InlineKeyboardMarkup(inline_keyboard = [[
        InlineKeyboardButton(text = 'Назад', callback_data = 'set_name_anketa'),
        InlineKeyboardButton(text = 'Отмена', callback_data = 'cancel_anketa')]])
    await callback_query.message.answer("Введите Ваш возраст", reply_markup=markup)

@router.message(Anketa.gender)
async def set_age_by_anketa_handler(message: Message, state:FSMContext):
    await state.update_data(gender=message.text)
    await message.answer(str(await state.get_data()))
    await state.clear()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await bot.set_my_commands([
        BotCommand(command='start', description='Запуск бота'),
        BotCommand(command='help', description='Справка'),
        BotCommand(command='delete', description='Отчислиться')])
    inline_markup = InlineKeyboardMarkup(inline_keyboard = [
        [InlineKeyboardButton(text = 'Вперёд', callback_data = 'next')]])
    await message.answer("Страница 1", reply_markup=inline_markup)

@router.callback_query(F.data == 'next')
async def next_handler(callback_query: CallbackQuery):
    inline_markup = InlineKeyboardMarkup(inline_keyboard = [
        [InlineKeyboardButton(text = 'Назад', callback_data = 'back')]])
    await callback_query.message.delete()
    await callback_query.message.answer(text='Страница 2', reply_markup=inline_markup)

@router.callback_query(F.data == 'back')
async def back_handler(callback_query: CallbackQuery):
    inline_markup = InlineKeyboardMarkup(inline_keyboard = [
        [InlineKeyboardButton(text = 'Вперёд', callback_data = 'next')]])
    await callback_query.message.delete()
    await callback_query.message.answer(text='Страница 1', reply_markup=inline_markup)

async def main():
    await dp.start_polling(bot)

dp.include_router(router)


if __name__ == "__main__":
    asyncio.run(main())
