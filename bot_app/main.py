import logging
from aiogram import Bot, Dispatcher, executor, types
from io import BytesIO
from PIL import Image
from models_utils import input_img_to_array, pca_reduce, predict_image
import pickle
from sklearn.decomposition import PCA
from sklearn.svm import SVC

API_TOKEN = '6921521470:AAHIi_d2An9GRsaHx83ogPw0nVUPQk7uRLs'  

model_path = 'model_svc.pkl'

with open(model_path, 'rb') as m:
    model = pickle.load(m)

join_files('model_pca.pkl', 'model', 'model_reconstructed.pkl')
pca_transform_path = 'model_reconstructed.pkl'

with open(pca_transform_path, 'rb') as pca:
    pca_transform = pickle.load(pca)

# Настройка логгирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Функция классификации изображения 
async def classify_image(image):
    one_d_image = input_img_to_array(image)
    img_pca = pca_reduce(pca_transform,one_d_image)
    predict_class = predict_image(model, img_pca)
    logging.info(f'{predict_class}')
    return predict_class

# Хендлер для команды /send_photo
@dp.message_handler(commands=['send_photo'])
async def request_photo(message: types.Message):
    await message.reply("Пожалуйста, отправьте фото для классификации.")

# Хендлер для получения фото
@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    photo_bytes = BytesIO()
    await message.photo[-1].download(destination_file=photo_bytes)
    photo_bytes.seek(0)
    image = Image.open(photo_bytes)

    # Вызов функции классификации
    classification_result = await classify_image(image)
    await message.reply(f"Результат классификации: {classification_result}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
