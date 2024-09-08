# Hostal-Oleo Demand Prediction

Welcome to the **Hostal-Oleo Demand Prediction** project! This repository contains the full pipeline for predicting the demand of an 8-room hostel based on historical booking data collected via the **WuBook Zak API**. The goal is to provide an efficient and scalable solution that optimizes pricing strategies to maximize revenue.

## 🚀 Project Overview

This project is part of my portfolio, showcasing a **machine learning pipeline** that handles everything from data collection to model training and inference. With the help of the WuBook API, the model predicts future demand for the hostel, enabling better pricing and management decisions.

### Key Features:
- **Data Collection**: Automates data extraction from the WuBook Zak API.
- **Data Preparation**: Cleans and processes the data to make it ready for modeling.
- **Model Training**: Uses historical booking data to train a machine learning model for demand forecasting.
- **Inference**: Predicts future demand to optimize booking strategies.
- **Scalability**: Can be adapted to other small and medium-sized hospitality businesses.

## 📊 Machine Learning Workflow

1. **Data Collection**: 
   - Extracts data such as booking dates, cancellations, room availability, and seasonal trends using the WuBook Zak API.

2. **Data Preprocessing**:
   - Cleans the data by handling missing values, removing outliers, and creating new features like booking lead time and day of the week effects.

3. **Model Training**:
   - Trains models such as Random Forest, Gradient Boosting, or XGBoost, depending on performance metrics.
   - Validates model performance using cross-validation and fine-tunes using grid search.

4. **Demand Prediction**:
   - Outputs daily demand predictions, which are then used to inform pricing strategies.

## 🛠️ Tech Stack

- **Languages**: Python
- **Libraries**: 
  - `scikit-learn`
  - `pandas`
  - `numpy`

- **API**: WuBook Zak API
- **Modeling**: Machine Learning 
- **Environment Management**: Poetry
