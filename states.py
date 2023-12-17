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

class FSMGuestStates(StatesGroup):
    guest_default = State()
    password = State()

# Твои состояния, Женя. Я подумал стоит немного переделать// стирай их нафиг
class FSMRidenshi(StatesGroup):
    fill_login = State()  # Состояние ожидания ввода логина
    fill_password = State()  # Состояние ожидания ввода пароля
    fill_topic = State()  # Состояние ожидания выбора темы косяка
    fill_over_topic = State()  # состояние ожидание ввода иной темы косяка
    # upload_photo = State()     # Состояние ожидания загрузки фото
    fill_desc = State()  # Состояние ожидания ввода описания
    down_topic_selection = State()  # Состояние ожидания ввода подтемы
    down_down_topic_selection = State()  # Состояние ожидания ввода подтемы
    faq = State()  # Состояние вывода faq
    fill_request = State()  # Состояние составления запроса в поддержку
    send_request = State()  # Состояние отправки запроса
    faq_select = State()


class FSMAdminStates(StatesGroup):
    admin_default = State()  # Пользователь является сотрудником (администратором)
