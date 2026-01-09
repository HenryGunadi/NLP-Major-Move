import httpx
from typing import List
from utils import safe_get, clean_text
from pathlib import Path
from models.fin_bert import MultiTaskFinBert
import torch
from transformers import BertTokenizer

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "models" / "finbert"

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
                    "min_match_score": 70
                }
            )
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"{self.__class__.__name__} get_news() error : {str(e)}")
            return None

    def format_news(self, news):
        try:
            formatted = []

            for item in news:
                entities = item.get("entities", [])

                formatted.append({
                    "text": f"{item.get('title','')}. "
                            f"{item.get('description','')}. "
                            f"{item.get('snippet','')}. "
                            f"Keywords: {item.get('keywords','')}.",
                    "symbols": [e["symbol"] for e in entities],
                    "published_at": item.get("published_at"),
                    "source": item.get("source"),
                    "url": item.get("url")
                })

            return formatted
        except Exception as e:
            print(f"{self.__class__.__name__} format_news() error : {str(e)}")
            return []

class FinBERT:
    def __init__(self, model_path: Path):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = MultiTaskFinBert.from_pretrained(model_path)

        self.model.to(self.device)
        self.model.eval()

        self.sentiment_id2label = {
            0: "Negative",
            1: "Neutral",
            2: "Positive",
        }

        self.importance_id2label = {
            0: "non-major",
            1: "major",
        }

    @torch.no_grad()
    def predict(self, text: str):
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128,
        )

        input_ids = inputs["input_ids"].to(self.device)
        attention_mask = inputs["attention_mask"].to(self.device)

        sentiment_logits, importance_logits = self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
        )

        # Get predictions and confidence scores
        sentiment_probs = torch.softmax(sentiment_logits, dim=1)
        importance_probs = torch.softmax(importance_logits, dim=1)
        
        sentiment_id = torch.argmax(sentiment_logits, dim=1).item()
        importance_id = torch.argmax(importance_logits, dim=1).item()
        
        sentiment_score = sentiment_probs[0][sentiment_id].item()
        importance_score = importance_probs[0][importance_id].item()

        return {
            "headline": text,
            "sentiment": self.sentiment_id2label[sentiment_id],
            "sentiment_score": round(sentiment_score * 100, 2),
            "importance": self.importance_id2label[importance_id],
            "importance_score": round(importance_score * 100, 2),
        }