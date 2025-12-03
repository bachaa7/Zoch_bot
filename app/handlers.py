from aiogram import F, Router
from aiogram.types import Message, CallbackQuery,ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command , StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import types

from app.keyboards import DefinitionCallbackFactory
from app.keyboards import definitions_keyboard
from add_defiition import add_definition_to_concept
from app.keyboards import add_concept_button
from app.keyboards import concept_button
from app.keyboards import concept_lookup_button
from app.calorie_calculator import *

import app.keyboards as kb
from app.reminder_instance import reminder_manager
from app.reminder_instance import get_reminder_manager

from app.user_utils import UserManager
from app.definition_handler import get_definition_command


router = Router()

# Стейт для регистрации
class Register(StatesGroup):
    name = State()
    age = State()
    number = State()


class CalorieCalculation(StatesGroup):
    age = State()
    gender = State()
    weight = State()
    height = State()
    activity_level = State()
    goal = State()


class ReminderStates(StatesGroup):
    waiting_for_times = State()


@router.message(CommandStart())  # Обработчик команды /start
async def cmd_start(message: Message):
    await message.answer(
        "🕐 Доброго времени суток!\n\n"
        "Я ваш персональный ассистент для управления здоровьем и продуктивностью.\n\n"
        "Доступные возможности:\n"
        "🔹 /register - Пройти регистрацию\n"
        "🔹 /profile - Посмотреть свой профиль\n" 
        "🔹 /delete_me - Удалить аккаунт\n\n"
        "Используйте команды или интерактивное меню для навигации.", 
        reply_markup=kb.main)
    #await message.reply('Вас приветсвует ваш персональный ассистент воспользуйтесь одной из команд или встроенной клавиатурой')

@router.message(Command('help'))  
async def cmd_help(message: Message):
    await message.answer("Вы нажали на кнопку помощи. Если у вас возникли какие-то проблемы, то можете связаться с нами walkyn9@gmail.com")


@ router.message(F.text == "о системе")
async def about_system(message: Message):
    await message.answer("Позже будет добавлена информация о системе")


# # Обработчик текста "о нас"
# @router.message(F.text == "о нас")
# async def about_us(message: Message):
#     await message.answer("Выберите человека ", reply_markup=kb.about_us)

# # Callback для выбора Казаченко
# @router.callback_query(F.data == 'Kazachenka')
# async def Kazachenka(callback: CallbackQuery):
#     await callback.answer("Вы выбрали Казаченко", show_alert=True)
#     await callback.message.answer("Казаченко Вадим Александрович - студент БГУИР")

# # Callback для выбора Ковальчука
# @router.callback_query(F.data == 'Kovalchyk')
# async def Kovalchyk(callback: CallbackQuery):
#     await callback.answer("Вы выбрали Овна", show_alert=True)
#     await callback.message.answer("Ковальчук Виктория - любит помацать пяточки.")

# # Callback для выбора Черетука
# @router.callback_query(F.data == 'Cheretyk')
# async def Cheretyk(callback: CallbackQuery):
#     await callback.answer("Вы выбрали Тимофея", show_alert=True)
#     await callback.message.answer("Черетун - Минский Messi.")



@router.message(F.text == "Поиск определения")
async def about_us(message: Message):
    await message.answer("Выберите: ", reply_markup=kb.concept_lookup_button())






# Обработчик текста "Функционал"
@router.message(F.text == "Функционал")
async def about_us(message: Message):
    await message.answer("Выберите функционал: ", reply_markup=kb.fuction_keyboard)
    

@router.callback_query(F.data == 'calculate_calories')
async def handle_calculate_calories(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите ваш возраст:")
    await state.set_state(CalorieCalculation.age.state)


# Обработчик для ввода возраста
@router.message(CalorieCalculation.age)
async def get_age(message: Message, state: FSMContext):
    try:
        age = int(message.text)
        if age <= 0:
            raise ValueError("Возраст должен быть положительным числом.")
        await state.update_data(age=age)
        await message.answer("Введите ваш пол (M/W):")
        await state.set_state(CalorieCalculation.gender.state)
    except ValueError:
        await message.answer("Пожалуйста, введите корректный возраст (целое положительное число).")


# Обработчик для ввода пола
@router.message(CalorieCalculation.gender)
async def get_gender(message: Message, state: FSMContext):
    gender = message.text.strip().lower()
    if gender not in ['m', 'w']:
        await message.answer("Пожалуйста, введите корректный пол (M или W).")
        return
    await state.update_data(gender=gender)
    await message.answer("Введите ваш вес (кг):")
    await state.set_state(CalorieCalculation.weight.state)

# Обработчик для ввода веса
@router.message(CalorieCalculation.weight)
async def get_weight(message: Message, state: FSMContext):
    try:
        weight = float(message.text)
        if weight <= 0:
            raise ValueError("Вес должен быть положительным числом.")
        await state.update_data(weight=weight)
        await message.answer("Введите ваш рост (см):")
        await state.set_state(CalorieCalculation.height.state)
    except ValueError:
        await message.answer("Пожалуйста, введите корректный вес (положительное число).")
 


# Обработчик для ввода роста
@router.message(CalorieCalculation.height)
async def get_height(message: Message, state: FSMContext):
    try:
        height = float(message.text)
        if height <= 0:
            raise ValueError("Рост должен быть положительным числом.")
        await state.update_data(height=height)
        await message.answer("Введите уровень активности (1 - низкий, 2 - средний, 3 - высокий):")
        await state.set_state(CalorieCalculation.activity_level.state)
    except ValueError:
        await message.answer("Пожалуйста, введите корректный рост (положительное число).")


@router.message(CalorieCalculation.activity_level)
async def get_activity_level(message: Message, state: FSMContext):
    activity_level = int(message.text)
    if activity_level < 1 or activity_level > 3:
        raise ValueError("Уровень активности должен быть от 1 до 3.")
    await state.update_data(activity_level=activity_level)
    await message.answer('Введите вашу цель: похудение / набор / поддержание:')
    await state.set_state(CalorieCalculation.goal.state)


# Обработчик для ввода уровня активности
@router.message(CalorieCalculation.goal)
async def get_goal(message: Message, state: FSMContext):
    goal = message.text.strip().lower()
    await state.update_data(goal=goal)
    user_data = await state.get_data()
    age = user_data['age']
    gender = user_data['gender']
    weight = user_data['weight']
    height = user_data['height']
    activity_level = user_data['activity_level']

    bmr = calculate_bmr(age, gender, weight, height)
    calories = calculate_calories(bmr, activity_level)
    adjusted = adjust_calories_for_goal(calories, goal)
    bmi, classification = calculate_bmi(weight, height)
    proteins, fats, carbs = calculate_macronutrients(adjusted, gender)

    await message.answer(
        f'Ваша суточная норма калорий для цели "{goal}": {adjusted:.2f} ккал\n'
        f'Индекс массы тела (ИМТ): {bmi} — {classification}\n\n'
        f'Рекомендуемое суточное потребление БЖУ:\n'
        f'Белки: {proteins} г\n'
        f'Жиры: {fats} г\n'
        f'Углеводы: {carbs} г'
    )
    await state.clear()




# === Напоминания ===


# Обработчик кнопки "Установить напоминания"
@router.callback_query(F.data == 'set_reminders')
async def start_reminder_menu(callback: CallbackQuery):
    await callback.message.answer("Выберите тип напоминания:", reply_markup=kb.reminder_type_keyboard)
    await callback.answer()

# Обработчик выбора типа напоминания
@router.callback_query(F.data.in_({"reminder_water", "reminder_sleep", "reminder_exercise"}))
async def select_reminder_type(callback: CallbackQuery, state: FSMContext):
    reminder_map = {
        "reminder_water": "water",
        "reminder_sleep": "sleep",
        "reminder_exercise": "exercise"
    }
    reminder_type = reminder_map[callback.data]

    await state.update_data(reminder_type=reminder_type)
    await callback.message.answer(f"Введите время для напоминаний о {reminder_type} (например: 08:00 или 08:00, 22:00):")
    await state.set_state(ReminderStates.waiting_for_times)
    await callback.answer()




# Обработчик ввода времени напоминаний
@router.message(StateFilter(ReminderStates.waiting_for_times))
async def set_reminder_times(message: Message, state: FSMContext):
    data = await state.get_data()
    reminder_type = data.get("reminder_type")
    times = [t.strip() for t in message.text.split(",")]

    chat_id = message.chat.id
    try:
        # Добавляем напоминания через ReminderManager
        reminder_manager = get_reminder_manager()
        reminder_manager.add_reminder(chat_id, reminder_type, times)
        await message.answer(f"Напоминания о {reminder_type} установлены на: {', '.join(times)}")
    except Exception as e:
        await message.answer(f"Ошибка при установке напоминаний: {e}")

    await state.clear()



# @router.message(Command('registers'))
# async def register(message: Message, state: FSMContext):
#     # Проверяем регистрацию с проверкой структуры данных
#     if await UserManager.is_registered(message.from_user.id):
#         await message.answer("Вы уже зарегистрированы!")
#         return
    
#     await state.set_state(Register.name)
#     await message.answer("Введите ваше имя:")

# @router.message(Register.name)
# async def register_name(message: Message, state: FSMContext):
#     if not message.text:
#         await message.answer("Пожалуйста, введите текст")
#         return
        
#     await state.update_data(name=message.text)
#     await state.set_state(Register.age)
#     await message.answer("Введите ваш возраст:")

# @router.message(Register.age)
# async def register_age(message: Message, state: FSMContext):
#     if not message.text:
#         await message.answer("Пожалуйста, введите текст")
#         return
        
#     await state.update_data(age=message.text)
#     await state.set_state(Register.number)
#     await message.answer("Отправьте ваш номер телефона:", reply_markup=kb.get_number)

# @router.message(Register.number, F.contact)
# async def register_number(message: Message, state: FSMContext):
#     data = await state.get_data()
#     phone = message.contact.phone_number
    
#     # Формируем данные для сохранения
#     user_data = {
#         'name': data.get('name'),
#         'age': data.get('age'),
#         'phone': phone
#     }
    
#     # Создаем пользователя через UserManager
#     if await UserManager.create_user(message.from_user.id, user_data):
#         await message.answer(
#             f"✅ Регистрация завершена!\n"
#             f"Имя: {user_data['name']}\n"
#             f"Возраст: {user_data['age']}\n"
#             f"Телефон: {user_data['phone']}",
#             reply_markup=kb.remove()  # Убираем клавиатуру
#         )
#     else:
#         await message.answer(
#             "❌ Не удалось сохранить данные. Попробуйте позже",
#             reply_markup=kb.remove()
#         )
    
#     await state.clear()



# #####################################################################################
# @router.message(Command('profile'))
# async def show_profile(message: Message):
#     # Проверяем регистрацию с проверкой структуры
#     if not await UserManager.is_registered(message.from_user.id):
#         await message.answer("Сначала зарегистрируйтесь через /register")
#         return
    
#     # Получаем данные через UserManager
#     user_data = await UserManager.get_user_data(message.from_user.id)
    
#     if not user_data:
#         await message.answer("❌ Не удалось загрузить данные профиля")
#         return
        
#     await message.answer(
#         f"📌 Ваш профиль:\n"
#         f"Имя: {user_data.get('name', 'не указано')}\n"
#         f"Возраст: {user_data.get('age', 'не указан')}\n"
#         f"Телефон: {user_data.get('phone', 'не указан')}"
#     )

# @router.message(Command('delete_me'))
# async def delete_profile(message: Message):
#     if await UserManager.delete_user(message.from_user.id):
#         await message.answer("✅ Ваш профиль удален")
#     else:
#         await message.answer("❌ Не удалось удалить профиль")
# #######################################################################################










##################################           Рекомендации            ####################################################
@router.callback_query(F.data == 'recomendation')
async def send_recommend_menu_inline(callback: CallbackQuery):
    await callback.message.answer("Выберите категорию рекомендаций 👇", reply_markup=kb.recommend_keyboard)
    await callback.answer()

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
###############################################################################






################################# Понятия #####################################
@router.callback_query(lambda c: c.data == "show_concepts")
async def show_concepts(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите понятие:", reply_markup=definitions_keyboard())
    await callback.answer()



@router.message(F.text.lower() == "понятия")
async def send_concept_button(message: Message):
    await message.answer("Нажмите кнопку, чтобы выбрать понятие:", reply_markup=concept_button())



class AddConceptStates(StatesGroup):
    waiting_for_idtf = State()
    waiting_for_definition = State()

# Показываем кнопку
@router.message(F.text.lower() == "добавить понятие")
async def show_add_concept_button(message: types.Message):
    await message.answer("Нажмите, чтобы добавить новое понятие:", reply_markup=add_concept_button())

# Начинаем ввод
@router.callback_query(lambda c: c.data == "add_concept")
async def start_add_concept(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите идентификатор понятия:")
    await state.set_state(AddConceptStates.waiting_for_idtf)
    await callback.answer()

# Получаем IDTF
@router.message(AddConceptStates.waiting_for_idtf)
async def process_idtf(message: types.Message, state: FSMContext):
    await state.update_data(idtf=message.text.strip())
    await message.answer("Теперь введите определение для этого понятия:")
    await state.set_state(AddConceptStates.waiting_for_definition)

# Получаем определение и вызываем функцию
@router.message(AddConceptStates.waiting_for_definition)
async def process_definition(message: types.Message, state: FSMContext):
    data = await state.get_data()
    idtf = data['idtf']
    definition = message.text.strip()

    success = await add_definition_to_concept(idtf, definition)
    if success:
        await message.answer(f"✅ Понятие '{idtf}' с определением добавлено.")
    else:
        await message.answer(f"❌ Не удалось добавить определение для '{idtf}'.")

    await state.clear()




@router.callback_query(F.data == 'add_defenition')
async def show_add_definition_inline(callback: CallbackQuery):
    await callback.message.answer("Нажмите кнопку ниже для добавления определения:", reply_markup=kb.add_concept_button())
    await callback.answer()



@router.callback_query(F.data == 'found_defenition')
async def show_lookup_definition_inline(callback: CallbackQuery):
    await callback.message.answer(
        "Выберите понятие для просмотра определения:",
        reply_markup=kb.definitions_keyboard()  # Показываем кнопки с понятиями
    )
    await callback.answer()

# Новый обработчик для кнопок определений
@router.callback_query(F.data.startswith("define_"))
async def handle_definition_button(callback: CallbackQuery):
    # Извлекаем идентификатор из callback_data
    concept_id = callback.data.replace("define_", "")
    
    # Формируем "виртуальное" сообщение с командой /define
    class FakeMessage:
        def __init__(self, text):
            self.text = text
            self.answer = callback.message.answer
    
    # Создаем фейковое сообщение с командой
    fake_msg = FakeMessage(f"/define {concept_id}")
    
    # Вызываем ваш существующий обработчик команд
    await get_definition_command(fake_msg)
    await callback.answer()

##############################################################################################















class RegisterStates(StatesGroup):
    name = State()
    age = State()
    phone = State()


@router.message(Command("register"))
async def start_registration(message: Message, state: FSMContext):
    # if await UserManager.is_registered(message.from_user.id):
    #     await message.answer("Вы уже зарегистрированы! Используйте /profile")
    #     return
    
    await state.set_state(RegisterStates.name)
    await message.answer("Введите ваше имя:")

@router.message(RegisterStates.name)
async def process_name(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, введите текст")
        return
        
    await state.update_data(name=message.text)
    await state.set_state(RegisterStates.age)
    await message.answer("Введите ваш возраст:")

@router.message(RegisterStates.age)
async def process_age(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, введите текст")
        return
        
    await state.update_data(age=message.text)
    await state.set_state(RegisterStates.phone)
    await message.answer("Введите ваш телефон:")

@router.message(RegisterStates.phone)
async def process_phone(message: Message, state: FSMContext):
    phone = message.text
    if not phone:
        await message.answer("Пожалуйста, введите телефон")
        return
    
    user_data = await state.get_data()
    user_data['phone'] = phone
    
    if await UserManager.create_user(message.from_user.id, user_data):
        await message.answer(
            "✅ Регистрация завершена!\n"
            f"Имя: {user_data['name']}\n"
            f"Возраст: {user_data['age']}\n"
            f"Телефон: {phone}",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer("❌ Ошибка сохранения данных")
    
    await state.clear()

@router.message(Command("profile"))
async def show_profile(message: Message):
    if not await UserManager.is_registered(message.from_user.id):
        await message.answer("Вы еще не зарегистрированы. Используйте /register")
        return
    
    user_data = await UserManager.get_user_data(message.from_user.id)
    
    if not user_data:
        await message.answer("❌ Не удалось загрузить данные профиля")
        return
        
    await message.answer(
        "📌 Ваш профиль:\n"
        f"Имя: {user_data.get('name', 'не указано')}\n"
        f"Возраст: {user_data.get('age', 'не указан')}\n"
        f"Телефон: {user_data.get('phone', 'не указан')}"
    )

@router.message(Command("delete_me"))
async def delete_profile(message: Message):
    if not await UserManager.is_registered(message.from_user.id):
        await message.answer("Вы еще не зарегистрированы")
        return
    
    if await UserManager.delete_user(message.from_user.id):
        await message.answer("✅ Ваш профиль успешно удален")
    else:
        await message.answer("❌ Не удалось удалить профиль")


        

# @router.message(Command("register"))
# async def start_registration(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     print(f"DEBUG: User ID from message: {user_id}")
#     print(f"DEBUG: User first name: {message.from_user.first_name}")
    
#     if await UserManager.is_registered(user_id):
#         await message.answer("Вы уже зарегистрированы! Используйте /profile")
#         return
    
#     await state.set_state(RegisterStates.name)
#     await message.answer("Введите ваше имя:")




    # Добавляем в импорты
# from app.rag_creation_handlers import router as rag_creation_router

# Регистрируем роутер в main.py (будет показано ниже)

# Добавляем обработчик для кнопки "Управление знаниями"
@router.message(F.text == "📚 Управление знаниями")
async def knowledge_management(message: Message):
    """Управление знаниями для ИИ"""
    await message.answer(
        "📚 *Управление базой знаний ИИ-ассистента*\n\n"
        "Здесь вы можете добавлять информацию, которую ИИ будет использовать "
        "для ответов на вопросы о здоровье и образе жизни.\n\n"
        "Выберите действие:",
        reply_markup=kb.knowledge_management_keyboard()
    )