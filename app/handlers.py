from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb

router = Router()

# Стейт для регистрации
class Register(StatesGroup):
    name = State()
    age = State()
    number = State()

@router.message(CommandStart())  # Обработчик команды /start
async def cmd_start(message: Message):
    await message.answer('Доброго времени суток', reply_markup=kb.main)
    await message.reply('Вас приветсвует ваш персональный ассистент')

@router.message(Command('help'))  # Обработчик команды /help
async def cmd_help(message: Message):
    await message.answer("Вы нажали на кнопку помощи")

# Обработчик текста "о нас"
@router.message(F.text == "о нас")
async def about_us(message: Message):
    await message.answer("Выберите человека ", reply_markup=kb.about_us)

# Callback для выбора Казаченко
@router.callback_query(F.data == 'Kazachenka')
async def Kazachenka(callback: CallbackQuery):
    await callback.answer("Вы выбрали Казаченко", show_alert=True)
    await callback.message.answer("Казаченко Вадим Александрович - студент БГУИР")

# Callback для выбора Ковальчука
@router.callback_query(F.data == 'Kovalchyk')
async def Kovalchyk(callback: CallbackQuery):
    await callback.answer("Вы выбрали Овна", show_alert=True)
    await callback.message.answer("Ковальчук Виктория - персонаж еще полностью не открыт.")

# Callback для выбора Черетука
@router.callback_query(F.data == 'Cheretyk')
async def Cheretyk(callback: CallbackQuery):
    await callback.answer("Вы выбрали черта", show_alert=True)
    await callback.message.answer("Черетук (от слова ТУК) - ну такой мутный тип.")

# Обработчик текста "Функционал"
@router.message(F.text == "Функционал")
async def about_us(message: Message):
    await message.answer("Выберите функционал: ", reply_markup=kb.fuction_keyboard)

# Обработчик callback для выбора "расчет калорий"
@router.callback_query(F.data == 'calculate_calories')
async def calculate_calories(callback: CallbackQuery):
    await callback.answer("Вы выбрали рассчитать калории ", show_alert=True)
    await callback.message.answer("Функция расчета калорий пока не реализована.")

# Обработчик callback для выбора "мои данные"
@router.callback_query(F.data == 'my_data')
async def my_data(callback: CallbackQuery):
    await callback.answer("Вы выбрали просмотреть мои данные  ", show_alert=True)
    await callback.message.answer("Ваши данные пока не доступны.")

# Регистрация пользователя
@router.message(Command('register'))
async def register(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer("Введите ваше Имя: ")

@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.age)
    await message.answer("Введите ваш возраст")

@router.message(Register.age)
async def register_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Register.number)
    await message.answer("Отправьте ваш номер телефона", reply_markup=kb.get_number)

@router.message(Register.number, F.contact)
async def register_number(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    data = await state.get_data()
    await message.answer(f"Ваше имя: {data['name']}\n Ваш возраст: {data['age']}\n Номер: {data['number']}")
    await state.clear()

# Рекомендации
@router.message(F.text == "Рекомендации")
async def send_recommend_menu(message: Message):
    await message.answer("Выберите категорию рекомендаций 👇", reply_markup=kb.recommend_keyboard)

@router.callback_query(F.data == "food_recommend")
async def food_recommend(callback: CallbackQuery):
    await callback.message.answer(
        "🥣 **Завтрак** (07:00–09:00)\n"
        "✅ Овсянка на воде или молоке с фруктами\n"
        "✅ Яйца (варёные или омлет)\n"
        "✅ Тост из цельнозернового хлеба + авокадо\n"
        "⚖️ КБЖУ: 30% углеводы, 30% белки, 40% жиры\n\n"
        "🍲 **Обед** (12:00–14:00)\n"
        "✅ Отварная куриная грудка / рыба\n"
        "✅ Рис, киноа, гречка\n"
        "✅ Овощной салат с оливковым маслом\n"
        "⚖️ КБЖУ: 40% углеводы, 35% белки, 25% жиры\n\n"
        "🍽 **Ужин** (18:00–20:00)\n"
        "✅ Творог с ягодами или запечённые овощи с белком\n"
        "✅ Суп-пюре или омлет с зеленью\n"
        "⚖️ КБЖУ: 20% углеводы, 50% белки, 30% жиры\n\n"
        "🥛 **Перекус**\n"
        "✅ Орехи, яблоко, кефир, банан\n"
        "✅ Энергетические батончики без сахара",
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "habits_recommend")
async def habits_recommend(callback: CallbackQuery):
    await callback.message.answer(
        "🌿 Полезные привычки для здоровья:\n\n"
        "🚶‍♂️ Прогулка на свежем воздухе — **30 мин/день**\n"
        "💧 Пить **1.5–2 литра воды** в день\n"
        "😴 Ложиться до 23:00 и спать не менее 7–8 часов\n"
        "📴 Цифровой детокс: **1 час без телефона в день**\n"
        "🧘 Медитация/дыхательные практики — 5–10 мин\n"
        "🍏 Есть 4–5 раз в день, без переедания\n"
        "📓 Вести дневник питания и настроения (по желанию)",
        parse_mode="Markdown"
    )
    await callback.answer()

