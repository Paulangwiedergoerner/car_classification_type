# 🚗 Car Type Classification MLOps Dashboard

A professional Flask-based MLOps dashboard to monitor real-time AI predictions for car type classification. This project provides an interactive UI, real-time model insights, and fully styled charts and tables using Chart.js and Bootstrap 5.

---

## 📌 Project Overview

This dashboard is designed to visualize and manage AI predictions in real-time. It allows admins to:

- Monitor the number and types of car predictions.
- Analyze model behavior with clean, professional graphs.
- Filter predictions by date and car type.
- View all prediction entries in an organized, searchable table.

---

## 📊 Dataset

- **Source**: Custom labeled car images uploaded by users.
- **Structure**:
  - `image`: uploaded car image.
  - `label`: predicted car type.
  - `timestamp`: prediction date and time.
  - `duration`: model inference time in seconds.

This data is stored dynamically via a Flask backend and used to update the dashboard in real-time.

---

## ⚙️ Pipeline Steps

### 1. Data Preprocessing
- Images are resized and normalized before feeding into the model.
- Metadata (timestamp and duration) is stored alongside predictions.

### 2. Feature Engineering
- Additional metadata such as formatted time, top classes, and frequency stats are extracted for plotting and filtering.

### 3. Model Inference
- A pre-trained CNN or custom classifier is used to predict the car type.
- Prediction time is measured for performance tracking.

### 4. Visualization & Evaluation
- **Charts**: Four main Chart.js visualizations:
  - Car Type Distribution
  - Predictions Over Time
  - Top 5 Car Types
  - Prediction Time Distribution
- **KPIs**: Metrics at the top show total predictions, unique car types, top class, and latest prediction time.

### 5. Deployment
- Frontend: HTML + Bootstrap 5 + Chart.js
- Backend: Flask + SQLite
- Admin interface for monitoring live uploads and predictions.

---

## 🛠️ Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/car-type-classifier-dashboard.git
   cd car-type-classifier-dashboard
  
