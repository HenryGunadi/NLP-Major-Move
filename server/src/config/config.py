from pydantic import SecretStr
from pydantic_settings import BaseSettings
from pathlib import Path 

class AppConfig(BaseSettings):
  NEWS_API_TOKEN: SecretStr
  NEWS_API_BASE_URL: str

  class Config:
    env_file = Path(__file__).resolve().parent.parent.parent / ".env"

  @property
  def get_news_api_token(self):
    return self.NEWS_API_TOKEN.get_secret_value()

config = AppConfig()