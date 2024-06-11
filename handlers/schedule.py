from aiogram import Router, F
from aiogram.types import Message

from keyboards.main_menu import main_menu
from utils.api import get_schedule
from utils.models import Session, User

router = Router()


@router.message(F.text == "Показати минулий запит ⬇️")
async def find_schedule(message: Message):
    session = Session()
    user = session.query(User).filter(User.id == message.from_user.id).first()
    faculty = user.last_faculty
    course = user.last_course
    group = user.last_group

    data = await get_schedule(faculty, course, group)
    if data == {}:
        result = "📌 Пар немає"
        await message.answer(result, parse_mode='HTML')
    else:
        days = {
            'Понеділок': '<b>🗓 Понеділок</b>\n',
            'Вівторок': '<b>🗓 Вівторок</b>\n',
            'Середа': '<b>🗓 Середа</b>\n',
            'Четвер': '<b>🗓 Четвер</b>\n',
            "П'ятниця": "<b>🗓 П'ятниця</b>\n",
            'Субота': '<b>🗓 Субота</b>\n',
            'Неділя': '<b>🗓 Неділя</b>\n'
        }

        for date, info in data.items():
            result = ""
            result += f"<i>{days[info['day']]}</i> <code>({date})</code>\n"
            for lesson in info['schedule']:
                result += f"    🔹 Пара {lesson['lesson_number']} ({lesson['time'][0]} - {lesson['time'][1]})\n"
                result += f"    📖 Предмет: {lesson['subject']}\n"
                result += f"    👨‍🏫 Викладач: {lesson['lecturer']}\n"
                result += f"    🏫 Аудиторія: {lesson['audience'] if lesson['audience'] else 'Не вказано'}\n\n"
            await message.answer(result, parse_mode='HTML')