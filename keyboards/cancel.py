from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def cancel_button():
    # Створюємо список списків кнопок
    buttons = [
        [InlineKeyboardButton(text="Скасувати", callback_data="cancel")],
    ]

    # Створюємо об'єкт клавіатури з цим списком кнопок
    cancel_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return cancel_keyboard

