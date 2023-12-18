# Файл с состояниями
from aiogram.fsm.state import State, StatesGroup


# Состояния для регистрации (В практиках была авторизация - надо подумать)
class FSMUserRegTypes(StatesGroup):
    unregistered = State()  # Для незарегистрированных пользователей будет предложено зарегистрироватьсЯ
    select_position = State()  # Состояние ожидания выбора типа пользователя (сотрудник/препод./ ?студент?)
    fill_fullname = State()  # Состояние ожидания ввода пароля (для сотрудников / ?для преподавателей?)


class FSMUserStates(StatesGroup):
    user_default = State()
    choose_topic = State()
    choose_down_topic = State()
    fill_context = State()
    fill_name = State()

class FSMGuestStates(StatesGroup):
    guest_default = State()
    password = State()


class FSMAdminStates(StatesGroup):
    admin_default = State()  # Пользователь является сотрудником (администратором)
