from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_token : str
    openai_api_type : str
    openai_api_base : str
    openai_api_version : str
    deployment_name : str
    model_name : str
    client_id : str
    client_secret : str

    model_config = SettingsConfigDict(env_file=".env_api")

settings = Settings()

