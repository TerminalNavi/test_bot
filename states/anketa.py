from aiogram.fsm.state import State, StatesGroup

class Anketa(StatesGroup):
    '''Класс анкета. Мне кажется по названию всё понятно, 
    но если конкретнее - создаёт своеобразную запись,
    в которой есть три значения - имя, возраст, пол.'''
    name = State()
    age = State()
    gender = State()