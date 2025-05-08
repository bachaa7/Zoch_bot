from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import types

from app.keyboards import DefinitionCallbackFactory
from app.keyboards import definitions_keyboard
from add_defiition import add_definition_to_concept

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
    await message.answer("Вы нажали на кнопку помощи. Если вы надеетесь на помощь,то это не зря.")





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
    await callback.message.answer("Ковальчук Виктория - любит помацать пяточки.")

# Callback для выбора Черетука
@router.callback_query(F.data == 'Cheretyk')
async def Cheretyk(callback: CallbackQuery):
    await callback.answer("Вы выбрали черта", show_alert=True)
    await callback.message.answer("Черетун - Минский Messi.")



@router.message(F.text == "Поиск определения")
async def about_us(message: Message):
    await message.answer("Выберите: ", reply_markup=kb.concept_lookup_button())






# Обработчик текста "Функционал"
@router.message(F.text == "Функционал")
async def about_us(message: Message):
    await message.answer("Выберите функционал: ", reply_markup=kb.fuction_keyboard)
    

# Обработчик callback для выбора "расчет калорий"
@router.callback_query(F.data == 'calculate_calories')
async def calculate_calories(callback: CallbackQuery):
    await callback.answer("Вы выбрали рассчитать калории ", show_alert=True)
    await callback.message.answer("Функция расчета калорий пока не реализована.")


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
# @router.message(F.text == "Рекомендации")
# async def send_recommend_menu(message: Message):
#     await message.answer("Выберите категорию рекомендаций 👇", reply_markup=kb.recommend_keyboard)

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





@router.callback_query(lambda c: c.data == "show_concepts")
async def show_concepts(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите понятие:", reply_markup=definitions_keyboard())
    await callback.answer()


from app.keyboards import concept_button

@router.message(F.text.lower() == "понятия")
async def send_concept_button(message: Message):
    await message.answer("Нажмите кнопку, чтобы выбрать понятие:", reply_markup=concept_button())




from app.keyboards import add_concept_button


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




# @router.message(F.text.lower() == "добавить понятие")
# async def send_add_definition_button(message: Message):
#     await message.answer("Нажмите кнопку ниже, чтобы добавить определение:", reply_markup=add_concept_button())

@router.callback_query(F.data == 'add_defenition')
async def show_add_definition_inline(callback: CallbackQuery):
    await callback.message.answer("Нажмите кнопку ниже для добавления определения:", reply_markup=kb.add_concept_button())
    await callback.answer()






from app.keyboards import concept_lookup_button

class LookupConcept(StatesGroup):
    waiting_for_idtf = State()

# @router.message(F.text.lower() == "поиск определения")
# async def ask_for_concept(message: Message, state: FSMContext):
#     await message.answer("Нажмите кнопку ниже для поиска определения:", reply_markup=concept_lookup_button())

@router.callback_query(F.data == 'found_defenition')
async def show_lookup_definition_inline(callback: CallbackQuery):
    await callback.message.answer("Нажмите кнопку ниже для поиска определения:", reply_markup=kb.concept_lookup_button())
    await callback.answer()

@router.callback_query(F.data == "lookup_definition")
async def start_lookup(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите /define идентификатор понятия, определение которого вы хотите увидеть:")
    await state.set_state(LookupConcept.waiting_for_idtf)
    await callback.answer()
