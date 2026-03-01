import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_URL: str = os.getenv("BASE_URL", "https://reqres.in")
    API_VERSION: str = os.getenv("API_VERSION", "/api")
    API_KEY: str = os.getenv("API_KEY", "")
    EMAIL: str = os.getenv("EMAIL", "eve.holt@reqres.in")
    PASSWORD: str = os.getenv("PASSWORD", "cityslicka")
    REGISTER_EMAIL: str = os.getenv("REGISTER_EMAIL", "eve.holt@reqres.in")
    REGISTER_PASSWORD: str = os.getenv("REGISTER_PASSWORD", "pistol")
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "10"))

    @classmethod
    def base_api_url(cls) -> str:
        return f"{cls.BASE_URL}{cls.API_VERSION}"
