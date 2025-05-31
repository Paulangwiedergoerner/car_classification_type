from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np

# Load the pre-trained model
model = load_model("model/resnet50_car_body_type_model.h5")

# Class labels must match your training order
class_names = ['Convertible', 'Coupe', 'Hatchback', 'Pickup', 'SUV', 'Sedan', 'Van']

def predict_car_type(image_path):
    img = image.load_img(image_path, target_size=(224, 224))  # Update if your model uses different input shape
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize if needed

    predictions = model.predict(img_array)
    predicted_index = np.argmax(predictions[0])
    return class_names[predicted_index]
