import logging
import asyncio
import os

from aiogram import F, Router, Bot, Dispatcher
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from dotenv import load_dotenv
from requests_api import get_role, check_code_interact
from keyboards import get_host_keyboard, get_member_keyboard, get_link_to_interavctive, get_link_to_main_menu


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()


class CodeInput(StatesGroup):
    waiting_for_code = State()


MAX_ATTEMPTS = 2


@router.message(F.text == "/start")
async def start_handler(message: Message):

    role = await get_role(message)
    first_name = message.from_user.first_name

    if role == "leader":
        greet_text = (
            f"Приятно познакомиться, {first_name}! Вам назначена роль ведущего. "
            "В этом сервисе вы можете создавать, управлять и проводить интерактивы."
        )
        keyboard = get_host_keyboard()

    elif role == "participant":
        greet_text = (
            f"{first_name}, добро пожаловать в Clik! Вы подключились как участник — "
            "присоединяйтесь к интерактивам и проходите их с удовольствием."
        )
        keyboard = get_member_keyboard()

    else:
        greet_text = "Ваша роль не распознана. Пожалуйста, свяжитесь с администратором."
        keyboard = None

    await message.answer(greet_text, reply_markup=keyboard)


@router.message(F.text == "Управление интерактивами")
async def start_cmd(message: Message):
    if await get_role(message) == "leader":
        await message.answer("Панель управления интерактивами", reply_markup=get_link_to_main_menu())


@router.message(F.text == "Подключение к интерактиву")
async def start_cmd(message: Message, state: FSMContext):
    await state.set_state(CodeInput.waiting_for_code)
    await state.update_data(attempts=0)
    await message.answer("Введите код для подключения к интерактиву")


@router.message(CodeInput.waiting_for_code)
async def handle_code_input(message: Message, state: FSMContext):
    user_data = await state.get_data()
    attempts = user_data.get("attempts", 0)

    if await check_code_interact(message.text):
        await message.answer(
            "✅ Код верный! Подключайтесь к интерактиву! Скоро начнем!",
            reply_markup=get_link_to_interavctive()
        )
        return

    attempts += 1
    if attempts >= MAX_ATTEMPTS:
        await state.clear()
        await message.answer(
            "Попробуйте еще раз, нажав кнопку «Подключение к интерактиву»"
        )
    else:
        await state.update_data(attempts=attempts)
        await message.answer("Попробуйте ввести код еще раз")


@router.message(CommandStart(deep_link=True))
async def handle_start_with_param(message: Message, command: CommandObject):
    param = command.args
    if not param:
        return

    role = await get_role(message)
    is_valid_role = True
    keyboard = None

    if role == "leader":
        keyboard = get_host_keyboard()
        greeting = f"Получен код интерактива: {param}"

    elif role == "participant":
        keyboard = get_member_keyboard()
        greeting = f"Получен код интерактива: {param}"

    else:
        is_valid_role = False
        greeting = "Ваша роль не распознана. Пожалуйста, свяжитесь с администратором."

    await message.answer(greeting, reply_markup=keyboard)

    if is_valid_role:
        if await check_code_interact(param):
            await message.answer(
                "✅ Код верный! Подключайтесь к интерактиву! Скоро начнем!",
                reply_markup=get_link_to_interavctive()
            )
        else:
            await message.answer(
                "Код неверный, попробуйте ввести его вручную. Сначала нажмите кнопку \"Подключение к интерактиву\""
            )


dp.include_router(router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
