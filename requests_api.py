import certifi
import aiohttp
import os
import ssl

from dotenv import load_dotenv

load_dotenv()


# получение роли пользователя


async def get_role(message):
    url = "https://carclicker.ru/api/users/register"
    params = {
        "x_key": os.getenv("SECRET_KEY"),
        "telegram_id": message.from_user.id,
        "username": message.from_user.username,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "phone_number": ""
    }

    params = {k: v for k, v in params.items() if v is not None}

    # отключает проверку на подлинность ssl сертификата, иначе у меня на машине выдает ошибку
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    async with aiohttp.ClientSession() as session:
        async with session.post(url, params=params, ssl=ssl_context) as response:
            try:
                response_data = await response.json()
            except aiohttp.ContentTypeError:
                pass

            return response_data.get("role")


# функция проверки существования интерактива по коду (пока заглушка)


async def check_code_interact(code: str):
    url = "https://carclicker.ru/api/interactivities/join"
    payload = {"code": code}

    # async with aiohttp.ClientSession() as session:
    #     async with session.post(url, json=payload) as response:
    #         if response.status == 200:
    #             return True
    #         else:
    #             return False

    return code == "RTF2025"
