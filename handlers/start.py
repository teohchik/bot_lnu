from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.main_menu import main_menu
from utils.models import User, Session

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    session = Session()
    flag = session.query(User).filter(User.id == message.from_user.id).first()
    if flag is None:
        new_user = User(id=message.from_user.id)
        session.add(new_user)
        session.commit()
    session.close()
    await message.answer("Вітаю! Я - бот-розклад занять.", reply_markup=main_menu)
