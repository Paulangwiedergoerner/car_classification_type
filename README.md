# 🚗 Car Type Classification 

## 📘 Project Overview

This project is a **deep learning-powered car body type classifier** integrated into a Flask web application with a fully functional MLOps-style dashboard.

**Objectives:**
- Classify car images by body type (e.g., SUV, Coupe, Pickup) using a trained CNN model.
- Provide a user-friendly interface for uploading images and receiving predictions.
- Visualize predictions, model usage, and performance metrics in real-time via interactive charts.
- Enable admin-only access to a secure monitoring dashboard for insights and reporting.

---

## 📊 Dataset

**Source:** The dataset used for training the classification model is a curated collection of labeled car images scraped from various open datasets and online repositories.

**Classes Included:**
- Convertible  
- Coupe  
- SUV  
- Pickup  
- Minivan  
- Van  
- Hatchback  

**Dataset Structure:**
- Each class has ~500–1000 images.
- Images were resized to \(224 \times 224\) and normalized.
- Class labels were encoded and one-hot encoded for training.

---

## 🔄 Pipeline Steps

### 1. **Data Preprocessing**
- Resized images to `(224, 224, 3)` to match ResNet50 input requirements.
- Applied normalization using ImageNet mean/standard deviation.
- Used `ImageDataGenerator` for training/validation splits and augmentation (rotation, zoom, shift).

### 2. **Feature Engineering**
- Pretrained ResNet50 (without top layer) used as a feature extractor.
- Added custom dense layers with Dropout and ReLU activation.
- Output layer: softmax for multi-class classification.

### 3. **Model Training**
- Optimizer: Adam  
- Loss: categorical crossentropy  
- Epochs: 10–20  
- Metrics: Accuracy, Validation Accuracy  
- Trained using Keras with TensorFlow backend.

### 4. **Model Evaluation**
- Achieved >90% accuracy on the test set.
- Evaluated with confusion matrix and classification report.
- Saved final model as: `resnet50_car_body_type_model.h5`.

### 5. **Deployment**
- Loaded the model using Keras in a Flask backend.
- Developed a secure admin login system.
- Deployed using local Flask server; deployable to cloud (e.g., Heroku, AWS).

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/car-type-classifier.git
cd car-type-classifier
