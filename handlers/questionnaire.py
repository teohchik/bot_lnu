from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.cancel import cancel_button
from keyboards.possible_courses import generate_possible_groups_keyboard
from states.states import Form
from static_data.static import faculties, courses
from utils.api import get_group, get_schedule
from utils.models import Session, User

router = Router()


@router.message(F.text == "Знайти розклад 📅")
async def start_questionnaire(message: Message, state: FSMContext):
    text = ""
    for faculty in faculties:
        text += f"{faculty}. {faculties[faculty][0]}\n"
    await message.answer(f"Виберіть ваш факультет! Введіть цифру: \n\n{text}", reply_markup=await cancel_button())

    await state.set_state(Form.faculty)


@router.message(Form.faculty)
async def form_faculty(message: Message, state: FSMContext):
    try:
        user_faculty = faculties[int(message.text)]
    except (KeyError, ValueError):
        await message.answer("Факультет не знайдено! Напишіть ще раз:", reply_markup=await cancel_button())
        await state.set_state(Form.faculty)
        return
    await state.update_data(faculty=user_faculty[1])
    await state.set_state(Form.course)
    await message.answer("Тепер напишіть який ви курс:", reply_markup=await cancel_button())


@router.message(Form.course)
async def form_faculty(message: Message, state: FSMContext):
    try:
        if int(message.text) in courses:
            await state.update_data(course=message.text)
            await state.set_state(Form.group)
            await message.answer("Почніть вводити вашу групу:", reply_markup=await cancel_button())
        else:
            await message.answer("Значення має бути від 1 до 6, напишіть ще раз:", reply_markup=await cancel_button())
            await state.set_state(Form.course)
    except ValueError:
        await message.answer("Значення має бути цифрою, напишіть ще раз:", reply_markup=await cancel_button())
        await state.set_state(Form.course)


@router.message(Form.group)
async def form_faculty(message: Message, state: FSMContext):
    user_group = message.text
    data = await state.update_data()
    faculty = data["faculty"]
    course = data["course"]
    possible_groups = await get_group(faculty, course, user_group)
    if possible_groups is None:
        await message.answer("Такої групи не існує. Спробуйте ще раз:", reply_markup=await cancel_button())
        await state.set_state(Form.group)
    else:
        await message.answer(text="Можливі групи:",
                             reply_markup=await generate_possible_groups_keyboard(possible_groups))


@router.callback_query()
async def handle_callback_query(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "cancel":
        await callback_query.message.answer("Скасовано!")
        await state.clear()
    else:
        try:
            data = await state.update_data()
            faculty = data["faculty"]
            course = data["course"]
        except:
            return
        await state.clear()
        group = callback_query.data
        await callback_query.message.answer(f"Ви обрали {group}")

        session = Session()
        user = session.query(User).filter(User.id == callback_query.from_user.id).first()
        if user is not None:
            user.last_faculty = faculty
            user.last_course = course
            user.last_group = group
            session.add(user)
            session.commit()
        session.close()
        data = await get_schedule(faculty, course, group)
        if data == {}:
            result = "📌 Пар немає"
            await callback_query.message.answer(result, parse_mode='HTML')
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
                await callback_query.message.answer(result, parse_mode='HTML')
