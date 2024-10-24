from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    algorithm: str
    secret_key: str
    access_token_expire_minutes: int
    africas_talking_api_key: str
    africas_talking_username: str
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str

    # Use SettingsConfigDict for Pydantic v2
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

