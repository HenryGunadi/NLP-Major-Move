import httpx
from typing import List
from utils import safe_get, clean_text, load_model
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "models"

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
          "headline": f"{title}. {description}",
          "source": source
        }

        headlines.append(data_headline)

      return headlines
    
    except Exception as e:
      print(f"{self.__class__.__name__} format_news() error : {str(e)}")
      
class BaseModel:
  def predict(self, text):
    raise NotImplementedError
    
class MLogistic:
    def __init__(self, bundle):
        self.model = bundle["pipeline"]
        self.sentiment_le = bundle["sentiment_encoder"]
        self.importance_le = bundle["importance_encoder"]

    def predict(self, text: str):
        pred = self.model.predict([text])[0]

        sentiment = self.sentiment_le.inverse_transform([pred[0]])[0]
        importance = self.importance_le.inverse_transform([pred[1]])[0]

        return {
            "headline": text,
            "sentiment": sentiment,
            "importance": importance,
        }


class NaiveBayes(BaseModel):
  def __init__(self, model):
    self.model = model
    
  def predict(self, text):
    try:
      pass
    except Exception as e:
      print(f"{self.__class__.__name__} predict() error : {str(e)}")

class RandomForest(BaseModel):
  def __init__(self, model):
    self.model = model
    
  def predict(self, text):
    try:
      pass
    except Exception as e:
      print(f"{self.__class__.__name__} predict() error : {str(e)}")

class ModelManager:
    def __init__(self):
        self.current_model = None
        self.current_model_name = None 

    def set_model(self, model_name: str):
        if model_name == self.current_model_name:
          return self.current_model

        match model_name:
            case "mlogistic":
                self.current_model = MLogistic(
                  bundle=load_model(MODEL_PATH / "MultinomialLogisticRegresion.pkl"),
                )

                print("Success initialized : mlogistic model")
            case "nb":
                self.current_model = NaiveBayes(
                  model=None,
                )
            case "rf":
                self.current_model = RandomForest(
                  model=None,
                )
            case _:
                raise ValueError("Unknown model")

        self.current_model_name = model_name
        return self.current_model
    
    def predict(self, text):
        return self.current_model.predict(text)