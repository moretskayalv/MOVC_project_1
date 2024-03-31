import pickle
from pathlib import Path

import numpy as np

FILE = Path(__file__).resolve()
PARENT = FILE.parent

MODEL_PATH = str(PARENT / 'model_svc.pkl')
PCA_TRANSFORM_PARTS_DIR = str(PARENT / 'model')
PCA_TRANSFORM_PATH = str(PARENT / 'model_reconstructed.pkl')
CLASSES = {
    0: "на изображении присутствует Jerry",
    1: "на изображении присутствует Tom",
    2: "на изображении отсутствует и Tom и Jerry",
    3: "на изображении присутствуют и Tom и Jerry"
}


def input_img_to_array(input_image):
    """convert img to 1d (224*224*3) array"""
    data = []
    img = input_image
    img = img.resize((224, 224))
    img_array = np.array(img, dtype=float) / 255.0
    img_vector = img_array.flatten()
    data.append(img_vector)
    return np.array(data)


def pca_reduce(pca_weights, array):
    """reduce the number of features to 250"""
    reduced_array = pca_weights.transform(array)
    return reduced_array


def predict_image(model, reduced_array):
    """get the predicted class from the reduced array"""
    prediction = model.predict(reduced_array).tolist()[0]
    return CLASSES[prediction]


def join_files(parts_folder=PCA_TRANSFORM_PARTS_DIR, output_file_path=PCA_TRANSFORM_PATH):
    # if Path(output_file_path).exists():
    #     return
    parts_folder = Path(parts_folder)
    parts = [file.name for file in parts_folder.iterdir()]
    parts = sorted(parts, key=lambda x: int(x.split("_part")[1]))
    with open(output_file_path, 'wb') as output_file:
        for part_file_name in parts:
            part_file_path = Path(parts_folder, part_file_name)
            with open(part_file_path, 'rb') as part_file:
                output_file.write(part_file.read())


def load_model(model_path=MODEL_PATH):
    with open(model_path, 'rb') as m:
        model = pickle.load(m)
    return model


def load_transform(parts_folder=PCA_TRANSFORM_PARTS_DIR, output_file_path=PCA_TRANSFORM_PATH):
    if not Path(output_file_path).exists():
        join_files(parts_folder, output_file_path)
    with open(output_file_path, 'rb') as f:
        pca_transform = pickle.load(f)
    return pca_transform


def load_transform_and_model(
        model_path=MODEL_PATH,
        transform_parts_folder=PCA_TRANSFORM_PARTS_DIR,
        transform_file_path=PCA_TRANSFORM_PATH
):
    transform = load_transform(transform_parts_folder, transform_file_path)
    model = load_model(model_path)
    return transform, model


def classify_image(image):
    pca_transform, model = load_transform_and_model(MODEL_PATH, PCA_TRANSFORM_PARTS_DIR, PCA_TRANSFORM_PATH)
    one_d_image = input_img_to_array(image)
    img_pca = pca_reduce(pca_transform, one_d_image)
    predict_class = predict_image(model, img_pca)
    return predict_class