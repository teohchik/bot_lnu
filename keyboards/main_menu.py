# keyboards/main_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Знайти розклад 📅'),
            KeyboardButton(text='Показати минулий запит ⬇️')
        ]
    ],
    resize_keyboard=True
)