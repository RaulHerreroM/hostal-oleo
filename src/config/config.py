from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    api_key: str
    data_path_reservations: str
    data_path_df_days: str
    model_path: str
    
    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '.env')


settings = Settings()
