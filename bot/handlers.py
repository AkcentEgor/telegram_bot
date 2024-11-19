from aiogram import  Router, html
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import requests

router = Router()


class MoveMeter(StatesGroup):
    personal_account = State()
    meter = State()

class SetLastMeter(StatesGroup):
    personal_account = State()

    
@router.message(CommandStart())
async def command_start_handler(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Передать показания")],
            [KeyboardButton(text="Просмотреть последнее переданное показание счетчика")]
        ],
        resize_keyboard=True, # Делает кнопки компактнее
        row_width=1 # Количество кнопок в одном ряду
    )
    
    # Отправляем приветственное сообщение с клавиатурой             
    await message.answer(
                        f"Приветствую, {html.bold(message.from_user.full_name)}! С помощью этого бота можно передать показания вашего счетчика",
                        reply_markup=keyboard
    )
    
# Обработка нажатия на кнопки
        
@router.message(lambda message: message.text == "Передать показания")
async def process_button_click(message: Message, state: FSMContext):
    await state.set_state(MoveMeter.personal_account)
    await message.answer('Введите номер лицевого счёта')  
    
@router.message(MoveMeter.personal_account)
async def move_meter(message: Message, state: FSMContext):
    await state.update_data(personal_account=int(message.text))
    await state.set_state(MoveMeter.meter)
    await message.answer("Введите показания счётчика")
    
@router.message(MoveMeter.meter)
async def move_data_meter(message: Message, state: FSMContext):
    await state.update_data(meter=int(message.text))
    data = await state.get_data()
    body_request = data
    response = requests.post("http://api:8000",json=body_request)
    if response.status_code == 200:
        await message.answer("Показания успешно переданы!")
    await state.clear()
    

        
@router.message(lambda message: message.text == "Просмотреть последнее переданное показание счетчика")
async def process_button_click(message: Message, state: FSMContext):
    await state.set_state(SetLastMeter.personal_account)
    await message.answer('Введите номер лицевого счёта')  

@router.message(SetLastMeter.personal_account)
async def move_meter(message: Message, state: FSMContext):
    await state.update_data(personal_account=int(message.text))
    data = await state.get_data()
    body_request = data
    response = requests.get("http://api:8000",json=body_request)
    # Проверяем статус ответа
    if response.status_code == 200:
        response_data = response.json()  # Парсим JSON-ответ
        
        # Формируем сообщение для пользователя
        response_message = (
            f"Лицевой счет: {response_data.get('personal_account')}\n"
            f"Последнее переданное показание счетчика: {response_data.get('meter')}"
        )
        
        # Отправляем сообщение пользователю
        await message.answer(response_message)
    else:
        # Обрабатываем ошибки
        await message.answer(f"Ошибка при передаче данных: {response.status_code}")
    
    # Очищаем состояние
    await state.clear()