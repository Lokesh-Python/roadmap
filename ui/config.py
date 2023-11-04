from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    api_host : str
    api_roadmap_path : str
    api_questions_path : str
    api_username : str
    api_password : str

    model_config = SettingsConfigDict(env_file=".env_ui")

settings = Settings()

