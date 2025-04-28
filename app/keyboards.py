from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

# Основная клавиатура
main = ReplyKeyboardMarkup(
    keyboard=[
        [
         KeyboardButton(text='Функционал'),
         KeyboardButton(text='Рекомендации')
        ],
        [
            KeyboardButton(text='Контакты'),
            KeyboardButton(text='о нас')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню..."
)


# Клавиатура "о нас"
about_us = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Казаченко", callback_data='Kazachenka')],
        [InlineKeyboardButton(text="Черетук", callback_data='Cheretyk')],
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
        [InlineKeyboardButton(text="Мои данные", callback_data='my_data')]
    ]
)

recommend_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🍽 Питание", callback_data='food_recommend')],
        [InlineKeyboardButton(text="🌿 Полезные привычки", callback_data='habits_recommend')]
    ]
)
