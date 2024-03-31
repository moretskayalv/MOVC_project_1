import os
import sys
import logging
from io import BytesIO
from PIL import Image
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.filters import CommandStart

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bot.models_utils import classify_image

API_TOKEN = os.environ["API_TOKEN"]
START_MESSAGE = (
    "Привет! Я бот-классификатор изображений. "
    "Отправьте изображение с Томом или Джерри, я определю кто нарисован."
)

dp = Dispatcher()
bot = Bot(token=API_TOKEN)


@dp.message(CommandStart())
async def request_photo(message: types.Message):
    await message.reply(START_MESSAGE)


@dp.message(F.photo)
async def handle_photo(message: types.Message):
    photo_bytes = BytesIO()
    photo = message.photo[-1]
    await bot.download(photo.file_id, destination=photo_bytes)
    photo_bytes.seek(0)
    image = Image.open(photo_bytes)
    classification_result = classify_image(image)
    await message.reply(f"Результат классификации: {classification_result}")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
