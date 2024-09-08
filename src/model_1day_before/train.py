from src.config.config import settings
import pandas as pd
import os
import logging
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib

logging.basicConfig(level=logging.INFO)


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    df['date'] = pd.to_datetime(df['date'])
    df = pd.get_dummies(df, columns=['month', 'day_of_week'])
    return df


def split_train_test(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values('date')
    train = df.iloc[:int(len(df) * 0.8)]
    test = df.iloc[int(len(df) * 0.8):]

    logging.info(f"Train size: {len(train)}")
    logging.info(f"Test size: {len(test)}")
    return train, test


def drop_columns(df_train, df_test) -> pd.DataFrame:

    df_train_1_day_before = df_train.drop(columns=[
        'date', 'rooms_reserved_2_days_before',
        'rooms_reserved_3_days_before', 'rooms_reserved_5_days_before',
        'rooms_reserved_7_days_before', 'rooms_reserved_14_days_before',
        'rooms_reserved_30_days_before', 'rooms_reserved_90_days_before'
    ])
    
    df_test_1_day_before = df_test.drop(columns=[
        'date', 'rooms_reserved_2_days_before',
        'rooms_reserved_3_days_before', 'rooms_reserved_5_days_before',
        'rooms_reserved_7_days_before', 'rooms_reserved_14_days_before',
        'rooms_reserved_30_days_before', 'rooms_reserved_90_days_before'
    ])
    
    return df_train_1_day_before, df_test_1_day_before


def train_model(
        train: pd.DataFrame,
        test: pd.DataFrame) -> RandomForestRegressor:
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_squared_error

    X_train = train.drop(columns=['occupied_rooms'])
    y_train = train['occupied_rooms']

    X_test = test.drop(columns=['occupied_rooms'])
    y_test = test['occupied_rooms']

    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    mae = np.mean(np.abs(y_test - y_pred))
    logging.info(f"Mean Squared Error: {mse}, Mean Absolute Error: {mae}")

    return model


def build_train_1_day_before_model() -> pd.DataFrame:
    
    days_df = pd.read_csv(os.path.join(os.path.dirname(__file__),
                                       settings.data_path_df_days))
    days_df = prepare_data(days_df)
    train, test = split_train_test(days_df)
    train, test = drop_columns(train, test)
    model = train_model(train, test)
    joblib.dump(model, os.path.join(os.path.dirname(__file__),
                                    settings.model_path))
    pass


build_train_1_day_before_model()

