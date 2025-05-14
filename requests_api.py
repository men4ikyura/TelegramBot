import asyncio
import aiohttp

# функция для получения роли пользователя
# ответ роль пользователя


# Асинхронная функция для регистрации пользователя и получения его роли
# async def get_role(telegram_id, username, first_name, last_name, phone_number):
# url = "https://carclicker.ru/api/users/register"
# payload = {
#     "telegram_id": telegram_id,
#     "username": username,
#     "first_name": first_name,
#     "last_name": last_name,
#     "phone_number": phone_number
# }

# async with aiohttp.ClientSession() as session:
#     async with session.post(url, json=payload) as response:
#         if response.status == 200:
#             data = await response.json()
#             # Предположим, что в ответе есть поле "role"
#             return data.get("role", "роль не найдена")
#         else:
#             return f"Ошибка: {response.status}"
async def get_role(da):
    return "participant"


# функция проверки существования интерактива по коду
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
