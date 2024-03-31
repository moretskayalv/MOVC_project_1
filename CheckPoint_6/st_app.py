import streamlit as st
from PIL import Image
import io

from models_utils import classify_image 

# Заголовок приложения
st.title('Классификация изображений')

# Загрузчик файлов
uploaded_file = st.file_uploader("Выберите изображение...", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Чтение и отображение изображения
    image_bytes = io.BytesIO(uploaded_file.getvalue())
    img = Image.open(image_bytes)
    st.image(img, caption='Загруженное изображение', use_column_width=True)
    
    # Классификация изображения
    report = classify_image(img)
    
    # Отображение результатов
    st.write(f"Результат классификации: {report}")