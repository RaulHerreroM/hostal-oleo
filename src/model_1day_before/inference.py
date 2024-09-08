import pandas as pd
import os
from src.config.config import settings
import joblib
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    df['date'] = pd.to_datetime(df['date'])
    df = pd.get_dummies(df, columns=['month', 'day_of_week'])
    return df


def prepare_data_to_predict(df: pd.DataFrame) -> pd.DataFrame:
    data = df[df['date'] == datetime.now().date()+pd.DateOffset(days=1)]
    data = data.drop(columns=[
        'date', 'occupied_rooms', 'rooms_reserved_2_days_before',
        'rooms_reserved_3_days_before', 'rooms_reserved_5_days_before',
        'rooms_reserved_7_days_before', 'rooms_reserved_14_days_before',
        'rooms_reserved_30_days_before', 'rooms_reserved_90_days_before'
    ])
    return data


def inference():
    days_df = pd.read_csv(os.path.join(os.path.dirname(__file__),
                                       settings.data_path_df_days))
    df = prepare_data(days_df)
    df = prepare_data_to_predict(df)
    loaded_model = joblib.load(os.path.join(os.path.dirname(__file__),
                                            settings.model_path))
    prediction = loaded_model.predict(df)
    
    logging.info(f"Prediction for tomorrow: {prediction[0]}")
    return prediction

