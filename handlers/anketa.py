'''Куча важных модулей'''
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.anketa import Anketa
from keyboards.anketa import *

router = Router()

@router.message(Command("anketa"))
async def anketa_handler(message: Message, state:FSMContext):
    '''Стартует заполнение анкеты'''
    await state.set_state(Anketa.name)
    await message.answer("Введите Ваше имя", reply_markup=kb_anketa_cancel)

@router.callback_query(F.data == 'cancel_anketa')
async def cancel_handler(callback_query: CallbackQuery, state: FSMContext):
    """Единственный метод спасения от моего бота - кнопка отмена регистрации"""
    await state.clear()
    await callback_query.message.answer('Регистрация отменена')

@router.message(Anketa.name)
async def set_name_by_anketa_handler(message: Message, state:FSMContext):
    '''Сохраняет введённое имя и переходит на заполнения следующего пункта'''
    await state.update_data(name=message.text)
    await state.set_state(Anketa.age)
    await message.answer("Введите Ваш возраст", reply_markup=kb_anketa_cancel_and_back)

@router.callback_query(F.data == 'back_anketa')
async def back_anketa_handler(callback_query: CallbackQuery, state: FSMContext):
    '''Метод, позволяющий вернуться на заполнение предыдущего пункта анкеты'''
    current_state = await state.get_state()
    if current_state == Anketa.gender:
        await state.set_state(Anketa.age)
        await callback_query.message.answer(
            'Введите ваш возраст', reply_markup=kb_anketa_cancel_and_back)
    elif current_state == Anketa.age:
        await state.set_state(Anketa.name)
        await callback_query.message.answer(
            'Введите ваше имя', reply_markup=kb_anketa_cancel)


@router.message(Anketa.age)
async def set_age_by_anketa_handler(message: Message, state:FSMContext):
    '''Проверяет корректность ввода и сохраняет 
    введённые возраст.'''
    try:
        await state.update_data(age = int(message.text))
    except ValueError:
        await message.answer("Вы неверно ввели возраст")
        await message.answer(
            "Введите Ваш возраст", reply_markup=kb_anketa_cancel_and_back)
        return
    await state.set_state(Anketa.gender)
    await message.answer(
        "Выберите Ваш пол", reply_markup=kb_anketa_by_gender)

@router.callback_query(F.data.startwith('gender_') and Anketa.gender)
async def set_gender_anketa_handler(callback_query: CallbackQuery, state:FSMContext):
    '''Заносит в запись выбранный пол и выводит получившуюся анкету'''
    gender = {'gender_m':'Мужской', 'gender_w':'Женский'}[callback_query.data]
    await state.update_data(gender=gender)
    await callback_query.message.answer(str(await state.get_data()))
    await state.clear()

@router.message(Anketa.gender)
async def set_gender_by_anketa_handler(message: Message, state:FSMContext):
    '''Нажимать нужно кнопочки, а не свой гендер придумывать'''
    await message.answer('Нужно пол выбрать кнопкой')
