import pandas as pd
from datetime import timedelta


def get_occupied_rooms(day, df):
    occupied_rooms = df[(
        df['status'] == 'Confirmed') & 
        (df['dfrom'] <= day) &
        (df['dto'] > day)]
    return occupied_rooms['n_rooms'].sum()


def get_avg_price_per_room_and_day(day, df):
    occupied_rooms = df[(
        df['status'] == 'Confirmed') & 
        (df['dfrom'] <= day) & 
        (df['dto'] >= day)]
    
    total_price = 0
    total_rooms = 0
    
    for _, row in occupied_rooms.iterrows():
        num_days = (row['dto'] - row['dfrom']).days  
        total_price += row['total_price'] / num_days  
        total_rooms += row['n_rooms'] 
    
    if total_rooms == 0:
        return 0 
    
    return total_price / total_rooms


def fill_zero_with_neighbors(df):

    for i in range(len(df)):
        if df.loc[i, 'avg_price_per_room_filled'] == 0:

            prev_val = None
            next_val = None
            
            for j in range(i-1, -1, -1):
                if df.loc[j, 'avg_price_per_room_filled'] != 0:
                    prev_val = df.loc[j, 'avg_price_per_room_filled']
                    break
            
            for j in range(i+1, len(df)):
                if df.loc[j, 'avg_price_per_room_filled'] != 0:
                    next_val = df.loc[j, 'avg_price_per_room_filled']
                    break
            
            if prev_val is not None and next_val is not None:
                df.loc[i, 'avg_price_per_room_filled'] = (prev_val + next_val) / 2

            elif prev_val is not None:
                df.loc[i, 'avg_price_per_room_filled'] = prev_val

            elif next_val is not None:
                df.loc[i, 'avg_price_per_room_filled'] = next_val


def create_days_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df['status'] == 'Confirmed']

    df['created'] = pd.to_datetime(df['created'], format='%d/%m/%Y')
    df['dfrom'] = pd.to_datetime(df['dfrom'], format='%d/%m/%Y')
    df['dto'] = pd.to_datetime(df['dto'], format='%d/%m/%Y')

    min_date = df['dfrom'].min()
    max_date = df['dto'].max()

    df_days = pd.DataFrame({'date': pd.date_range(
        start=min_date, end=max_date)})
    
    df_days['occupied_rooms'] = df_days['date'].apply(
        lambda day: get_occupied_rooms(day, df))

    df_days['avg_price_per_room'] = df_days['date'].apply(
        lambda day: get_avg_price_per_room_and_day(day, df))

    anticipation_periods = [1, 2, 3, 5, 7, 14, 30, 90]

    for days in anticipation_periods:
        df_days[f'rooms_reserved_{days}_days_before'] = df_days['date'].apply(
            lambda day: df[
                (df['status'] == 'Confirmed') &
                (df['dfrom'] == day) & 
                (df['created'] == day - timedelta(days=days))  
            ]['n_rooms'].sum()
        )
    
    fill_zero_with_neighbors(df_days)
    df_days[df_days["occupied_rooms"] > 8]["occupied_rooms"] = 8

    df_days['month'] = df_days['date'].dt.month
    df_days['day_of_week'] = df_days['date'].dt.dayofweek
    df_days['occupied_rooms_1_day_ago'] = df_days['occupied_rooms'].shift(1)
    df_days['occupied_rooms_7_days_ago'] = df_days['occupied_rooms'].shift(7)

    return df_days