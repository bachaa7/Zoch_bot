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
            KeyboardButton(text='о нас'),
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
        [InlineKeyboardButton(text="Рассчитать калории ", callback_data='calculate_calories')],
        [InlineKeyboardButton(text='Рекомендации',callback_data='recomendation')],
        [InlineKeyboardButton(text="Поиск определения",callback_data='found_defenition')],
        [InlineKeyboardButton(text='Добавить понятие',callback_data='add_defenition')]
    ]
)

recommend_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🍽 Питание", callback_data='food_recommend')],
        [InlineKeyboardButton(text="🌿 Полезные привычки", callback_data='habits_recommend')]
    ]
)

def definitions_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Личная гигиена",
                callback_data=DefinitionCallbackFactory(concept_idtf="1_личная гигиена").json()  # Используем метод json()
            )],
            [InlineKeyboardButton(
                text="Психическое здоровье",
                callback_data=DefinitionCallbackFactory(concept_idtf="1_психическое здоровье").json()  # Используем метод json()
            )],


                        [
                InlineKeyboardButton(
                    text="Тимоха",  # ➕ Новое понятие
                    callback_data=DefinitionCallbackFactory(concept_idtf="Timoha").json()
                )
            ]

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





def concept_lookup_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔍 Посмотреть определение", callback_data="lookup_definition")]
    ])
