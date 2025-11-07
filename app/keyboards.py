from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from aiogram.filters.callback_data import CallbackData




class DefinitionCallbackFactory(CallbackData, prefix="definition"):
    concept_idtf: str



# Основная клавиатура
main = ReplyKeyboardMarkup(
    keyboard=[
        [
         KeyboardButton(text='Функционал')
         #KeyboardButton(text='Рекомендации')
        ],
        # [
        #  KeyboardButton(text="Поиск определения"),
        #  KeyboardButton(text='Добавить понятие')
        # ],
        [
            # KeyboardButton(text='о нас'),
            KeyboardButton(text='о системе')
            #KeyboardButton(text='Понятия')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню..."
)


# Клавиатура "о нас"
about_us = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Казаченко", callback_data='Kazachenka')],
        [InlineKeyboardButton(text="Черетун", callback_data='Cheretyk')],
        [InlineKeyboardButton(text='Ковальчук', callback_data='Kovalchyk')]
    ]
)


# Клавиатура для номера телефона
get_number = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отправьте номер", request_contact=True)]
    ],
    resize_keyboard=True
)


# Клавиатура функционала
fuction_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Рассчитать КБЖУ ", callback_data='calculate_calories')],
        [InlineKeyboardButton(text="Установить напоминание", callback_data='set_reminders')],
        [InlineKeyboardButton(text='Рекомендации',callback_data='recomendation')],
        [InlineKeyboardButton(text="Поиск определения",callback_data='found_defenition')],
        [InlineKeyboardButton(text='Добавить понятие',callback_data='add_defenition')]
    ]
)



reminder_type_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💧 Вода", callback_data="reminder_water")],
    [InlineKeyboardButton(text="🌙 Сон", callback_data="reminder_sleep")],
    [InlineKeyboardButton(text="🏃 Упражнения", callback_data="reminder_exercise")]
])



recommend_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🍽 Питание", callback_data='food_recommend')],
        [InlineKeyboardButton(text="🌿 Полезные привычки", callback_data='habits_recommend')]
    ]
)




# Кнопка для вызова понятий
def concept_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Выбрать понятие", callback_data="show_concepts")]
        ]
    )


def add_concept_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Добавить понятие", callback_data="add_concept")]
        ]
    )






def definitions_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Рекомендация по питанию",
                callback_data="define_food_recomend" 
            )],
            [InlineKeyboardButton(
                text="Личная гигиена",
                callback_data="define_personal_hygiene"
            )],

            [InlineKeyboardButton(
                text="Избежание вредных привычек",
                callback_data="define_nrel_avoidance_of_bad_habits"
            )],
            
            [InlineKeyboardButton(
                text="Гидратация",
                callback_data="nrel_hydration"
            )],

            [InlineKeyboardButton(
                text="Сон",
                callback_data="define_nrel_sleep"
            )],



            [InlineKeyboardButton(
                text="Питание",
                callback_data="define_nrel_nutrition"
            )],
            
            [InlineKeyboardButton(
                text="Активность",
                callback_data="define_physical_activity"
            )],

            [InlineKeyboardButton(
                text="Гигиена",
                callback_data="define_nrel_hygiene"
            )],





            [InlineKeyboardButton(
                text="Психическое здоровье", 
                callback_data="define_mental_health"
            )]
        ]
    )

def concept_lookup_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🔍 Посмотреть определение", 
            callback_data="show_definition_buttons"  
        )]
    ])