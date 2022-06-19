from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from pydantic import ValidationError
from modules.keyboard import Keyboard
from modules.fs_machine import Access
from modules.models import Regist
from loader import dp, interface


@dp.message_handler(commands=['menu', 'start'])
async def get_menu(message: Message):
	
	keyboard_item = [
		"Получить доступ",
		"Обновить токен доступа",
		"Документация к API"
	]
	kb = Keyboard.create_standart_keyboard(keyboard_item)
	answer = "Выберите вариант на клавиатуре"
	await message.answer(answer, reply_markup=kb)

@dp.message_handler(lambda message: message.text.startswith('Документация к API'))
async def get_docs(message: Message):
	keyboard_item = [
		"Получить доступ",
		"Обновить токен доступа",
		"Документация к API"
	]
	kb = Keyboard.create_standart_keyboard(keyboard_item)
	await message.answer("[Ссылка](http://finance-tracking.ru:8002/docs) на документацию", parse_mode='MARKDOWN', reply_markup=kb)
	

@dp.message_handler(lambda message: message.text.startswith('Получить доступ'))
async def get_name(message: Message):
	await message.answer("Введите фамилию и имя", reply_markup=ReplyKeyboardRemove())
	await Access.name.set()

@dp.message_handler(state = Access.name)
async def get_email(message: Message, state: FSMContext):
	await state.update_data({'model' : Regist(
		name=message.text
	)})
	await message.answer("Введите вашу почту")
	await Access.email.set()

@dp.message_handler(state = Access.email)
async def get_passwd(message: Message, state: FSMContext):
	data = await state.get_data()
	model = data.get("model")
	try:
		model.email = message.text
	except ValidationError:
		await message.answer("Введите корректный адрес почты")
		return
	else:
		await state.update_data({"model" : model})	
		await message.answer("Введите пароль")
		await Access.passwd.set()

@dp.message_handler(state = Access.passwd)
async def get_passwd(message: Message, state: FSMContext):
	data = await state.get_data()
	model = data.get("model")
	req = await interface.create_token(model.name, model.email, message.text)

	answer = f"Сохраните следующую информаци. Это токены для доступа к системе конроля личных расходов\n\nAccess Token: {req.access_token}\n\nRefresh Token: {req.refresh_token}"


	keyboard_item = [
		"Получить доступ",
		"Обновить токен доступа",
		"Документация к API"
	]
	kb = Keyboard.create_standart_keyboard(keyboard_item)

	await message.answer(answer, reply_markup=kb)

	await state.finish()