from pathlib import Path
from io import BytesIO
import pytest
from unittest.mock import patch, AsyncMock
from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE
from aiogram.filters import CommandStart
from aiogram import Bot
from aiogram.types import Message, User, Chat, PhotoSize

from bot.bot import handle_photo, request_photo, START_MESSAGE


FILE = Path(__file__).resolve()
PARENT = FILE.parent
SAMPLE_IMAGE = str(PARENT / 'test_jerry.jpg')


@pytest.mark.asyncio
async def test_request_photo():
    request = MockedBot(MessageHandler(request_photo, CommandStart()))
    calls = await request.query(MESSAGE.as_object(text="/start"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == START_MESSAGE


@pytest.mark.asyncio
async def test_handle_photo():
    user = User(id=123, is_bot=False, first_name="Test User")
    chat = Chat(id=123, type="private")
    photo = PhotoSize(file_id="fake_file_id", width=100, height=100, file_unique_id="unique_id")
    message = Message(message_id=1, from_user=user, chat=chat, photo=[photo], date=0)
    expected_classification_result = "на изображении присутствует Tom"
    with open(SAMPLE_IMAGE, "rb") as image_file:
        fake_image_bytes = BytesIO(image_file.read())
    fake_image_bytes.seek(0)
    with patch('bot.models_utils.classify_image', return_value=expected_classification_result), \
         patch.object(
             Bot, 'download', side_effect=lambda file_id, destination: destination.write(fake_image_bytes.read())
         ), \
         patch('aiogram.types.message.Message.reply', new_callable=AsyncMock) as mock_reply:
        await handle_photo(message)
        mock_reply.assert_awaited_with(f"Результат классификации: {expected_classification_result}")
