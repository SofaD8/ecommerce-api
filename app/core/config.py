from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Sofa`s eCommerce API"
    API_V1_STR: str = "/api/v1"


settings = Settings()
