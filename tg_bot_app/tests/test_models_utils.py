from pathlib import Path

import numpy as np
from unittest.mock import Mock
from PIL import Image

from bot.models_utils import input_img_to_array, pca_reduce, predict_image, classify_image, join_files, CLASSES


FILE = Path(__file__).resolve()
PARENT = FILE.parent
SAMPLE_IMAGE = str(PARENT / 'test_jerry.jpg')


def test_input_img_to_array():
    image = Image.new("RGB", (500, 500))
    result = input_img_to_array(image)
    assert result.shape == (1, 224*224*3)
    assert np.all(result >= 0) and np.all(result <= 1), "The array should be normalized"


def test_pca_reduce():
    pca_mock = Mock()
    pca_mock.transform.return_value = np.arange(250)[None, :]
    array = np.array([[1.0]*224*224*3])
    result = pca_reduce(pca_mock, array)
    assert result.shape == (1, 250), "PCA didn't reduce array to correct shape"


def test_predict_image():
    model_mock = Mock()
    model_mock.predict.return_value = np.array([1])
    array = np.arange(250)[None, :]
    result = predict_image(model_mock, array)
    model_mock.predict.assert_called_with(array)

    assert result == "на изображении присутствует Tom", "Prediction didn't match the correct class"


def test_classify_image():
    image = Image.open(SAMPLE_IMAGE)
    join_files()
    classes = list(CLASSES.values())
    classification_result = classify_image(image)

    assert classification_result in classes, f"Expected one of {', '.join(classes)}, got {classification_result}"
