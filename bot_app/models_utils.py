import numpy as np
from sklearn.decomposition import PCA
from sklearn.svm import SVC


def input_img_to_array(input_image):
  """convert img to 1d (224*224*3) array"""
  data = []
  img = input_image
  img = img.resize((224, 224))
  img_array = np.array(img, dtype=float) / 255.0  # Нормализация значений пикселей к диапазону [0, 1]
  img_vector = img_array.flatten()
  data.append(img_vector)
  return np.array(data)

def pca_reduce(pca_weights, array):
  """reduce the number of features to 250"""

  reduced_array = pca_weights.transform(array)
  return reduced_array

def predict_image(model, reduced_array):
  """get the predicted class from the reduced array"""
  instances = {0:"на изображении присутствует Jerry",
               1:"на изображении присутствует Tom",
               2:"на изображении отсутствует и Tom и Jerry",
               3:"на изображении присутствуют и Tom и Jerry"}
  prediction = model.predict(reduced_array).tolist()[0]
  return instances[prediction]
