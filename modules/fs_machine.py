from aiogram.dispatcher.filters.state import StatesGroup, State

class Access(StatesGroup):
    name = State()
    email = State()
    passwd = State()

class RefreshState(StatesGroup):
    email = State()
    refresh_token = State()
    responce_new_token = State()

