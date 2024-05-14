'''Необходимые для работы кода модули'''
import asyncio
import logging
# import datetime
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import Message, BotCommand, \
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup



bot_token = open('config.txt', encoding='UTF-8').readline()
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
    '''Класс анкета. Мне кажется по названию всё понятно, 
    но если конкретнее - создаёт своеобразную запись,
    в которой есть три значения - имя, возраст, пол.'''
    name = State()
    age = State()
    gender = State()

@router.message(Command("anketa"))
async def anketa_handler(message: Message, state:FSMContext):
    """Функция для получения имени того неполноценного индивида,
      решившего воспользоваться этим куском кода"""
    await state.set_state(Anketa.name)
    markup = InlineKeyboardMarkup(inline_keyboard = [[
        InlineKeyboardButton(text = 'Отмена', callback_data = 'cancel_anketa')]])
    await message.answer("Введите Ваше имя", reply_markup=markup)

@router.callback_query(F.data == 'cancel_anketa')
async def cancel_handler(callback_query: CallbackQuery, state: FSMContext):
    """Единственный метод спасения от моего бота - кнопка отмена регистрации"""
    await state.clear()
    await callback_query.message.answer('Регистрация отменена')

@router.message(Anketa.name)
async def set_name_by_anketa_handler(message: Message, state:FSMContext):
    """Странная фигня, объединяющая в себе две функции
      - запоминания имени, которое ввёл пользователь,
        и запрос на ввод его возраста."""
    await state.update_data(name=message.text)
    await state.set_state(Anketa.age)
    markup = InlineKeyboardMarkup(inline_keyboard = [[
        InlineKeyboardButton(text = 'Назад', callback_data = 'set_name_anketa'),
        InlineKeyboardButton(text = 'Отмена', callback_data = 'cancel_anketa')]])
    await message.answer("Введите Ваш возраст", reply_markup=markup)

@router.callback_query(F.data == 'set_name_anketa')
async def set_name_anketa_handler(callback_query: CallbackQuery, state: FSMContext):
    '''Самому бы понять, что это.
    Хотя не, знаю, есть под сообщением кнопочка назад, нажимаешь
    и бот опять отправляет запрос на ввод имени'''
    await anketa_handler(callback_query.message, state)

@router.message(Anketa.age)
async def set_age_by_anketa_handler(message: Message, state:FSMContext):
    '''Проверяет корректность ввода и сохраняет 
    введённые возраст.'''
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

@router.message(F.data == 'set_age_anketa')
async def set_age_anketa_handler(callback_query: CallbackQuery, state: FSMContext):
    '''Ещё одно обновление анкеты. Ещё одна кнопка назад. Только в этот раз возраст'''
    await state.set_state(Anketa.age)
    markup = InlineKeyboardMarkup(inline_keyboard = [[
        InlineKeyboardButton(text = 'Назад', callback_data = 'set_name_anketa'),
        InlineKeyboardButton(text = 'Отмена', callback_data = 'cancel_anketa')]])
    await callback_query.message.answer("Введите Ваш возраст", reply_markup=markup)

@router.message(Anketa.gender)
async def set_gender_by_anketa_handler(message: Message, state:FSMContext):
    await state.update_data(gender=message.text)
    await message.answer(str(await state.get_data()))
    await state.clear()

@router.message(Command("start"))
async def cmd_start(message: Message):
    '''Не помню что за фигня. Вроде просто создавали несколько
      команд для бота. Кстати, надо бы часть в своего бота забрать'''
    await bot.set_my_commands([
        BotCommand(command='start', description='Запуск бота'),
        BotCommand(command='help', description='Справка'),
        BotCommand(command='delete', description='Отчислиться'),
        BotCommand(command='anketa', description='Создание анкеты')])
    inline_markup = InlineKeyboardMarkup(inline_keyboard = [
        [InlineKeyboardButton(text = 'Вперёд', callback_data = 'next')]])
    await message.answer("Страница 1", reply_markup=inline_markup)

@router.callback_query(F.data == 'next')
async def next_handler(callback_query: CallbackQuery):
    '''То же самое, что с предыдущим, только тут создаётся сообщение
    с кнопкой под ней. Вызывает сообщение с кнопкой для вызова этого.
    Первоначальное сообщение удаляется.'''
    inline_markup = InlineKeyboardMarkup(inline_keyboard = [
        [InlineKeyboardButton(text = 'Назад', callback_data = 'back')]])
    await callback_query.message.delete()
    await callback_query.message.answer(text='Страница 2', reply_markup=inline_markup)

@router.callback_query(F.data == 'back')
async def back_handler(callback_query: CallbackQuery):
    '''Создаётся сообщение
    с кнопкой под ней. Вызывает сообщение с кнопкой для вызова этого.
    Первоначальное сообщение удаляется.'''
    inline_markup = InlineKeyboardMarkup(inline_keyboard = [
        [InlineKeyboardButton(text = 'Вперёд', callback_data = 'next')]])
    await callback_query.message.delete()
    await callback_query.message.answer(text='Страница 1', reply_markup=inline_markup)

async def main():
    '''Старт бота'''
    dp.include_routers(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
