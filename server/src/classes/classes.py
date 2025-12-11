import httpx
from typing import List
from utils import safe_get, clean_text

class NewsAPI:
  def __init__(self, api_key: str, base_url: str):
    self.api_key = api_key
    self.client = httpx.AsyncClient()
    self.base_url = base_url

  async def get_news(self, stock_symbol: str):
    try:
      response = await self.client.get(
                      f"{self.base_url}",
                      params={
                        "symbols": stock_symbol,
                        "api_token": self.api_key,
                        "filter_entities": "true",
                        "language": "en",
                        "min_match_score": 50
                      }
                    )
      
      response.raise_for_status()
      return response.json()
    except Exception as e:
      print(f"{self.__class__.__name__} get news() error : {str(e)}")

  def format_news(self, news):
    try:
      if news is None:
        return

      headlines = []

      for headline in news:
        title = clean_text(safe_get(headline, "title", None))
        description = clean_text(safe_get(headline, "description", None))

        if not (title or description):
          continue

        source = safe_get(headline, "url", None)
        data_headline = {
          "title": title,
          "description": description,
          "source": source
        }

        headlines.append(data_headline)

      return headlines
    
    except Exception as e:
      print(f"{self.__class__.__name__} format_news() error : {str(e)}")

    
class MachineLearningModel:
  def __init__(self, model):
    self.model = model

  def predict(self, data) -> List[dict]:
    try:
      return []
    except Exception as e:
      print(f"{self.__class__.__name__} predict() error : {str(e)}")