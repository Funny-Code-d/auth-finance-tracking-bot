from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from pydantic import ValidationError
from modules.keyboard import Keyboard
from modules.fs_machine import RefreshState
from modules.models import RefreshModel
from loader import dp, interface


@dp.message_handler(lambda message: message.text.startswith('Обновить токен доступа'))
async def start_refresh(message: Message):

    await message.answer("Введите Email", reply_markup=ReplyKeyboardRemove())
    await RefreshState.email.set()

@dp.message_handler(state = RefreshState.email)
async def get_email(message: Message, state: FSMContext):

    model = None
    try:
        model = RefreshModel(
            email=message.text
        )
    except ValidationError:
        await message.answer("Введите корректный Email")
        return
    else:
        await state.update_data({"model" : model})
        await message.answer("Введите Refresh Token")
        await RefreshState.refresh_token.set()
    
@dp.message_handler(state = RefreshState.refresh_token)
async def get_refresh_token(message: Message, state: FSMContext):
    
    data = await state.get_data()
    model = data.get("model")
    new_refresh_token = await interface.refresh_token(model.email, message.text)

    keyboard_item = [
		"Получить доступ",
		"Обновить токен доступа",
        "Документация к API"
	]
    kb = Keyboard.create_standart_keyboard(keyboard_item)

    if new_refresh_token:
        await message.answer(f"Новый токен доступа:\n\nAccess Token: {new_refresh_token}", reply_markup=kb)
    else:
        await message.answer("Email или refresh_token введены не правильно", reply_markup=kb)

    await state.finish()