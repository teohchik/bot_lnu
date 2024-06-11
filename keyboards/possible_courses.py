from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def generate_possible_groups_keyboard(possible_groups):
    # Створюємо список списків кнопок
    buttons = [
        [InlineKeyboardButton(text=group, callback_data=group)]
        for group in possible_groups
    ]

    # Створюємо об'єкт клавіатури з цим списком кнопок
    possible_group_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return possible_group_keyboard

