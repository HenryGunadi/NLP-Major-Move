from fastapi import APIRouter
from schemas import PredictResponse, PredictRequest
from classes import NewsAPI, FinBERT
from utils import safe_get

class MainRoute():
    def __init__(self, news_api_service: NewsAPI, model: FinBERT):
        self.router = APIRouter()
        self.news_api_service = news_api_service
        self.model = model
    
        @self.router.post("/predict", response_model=PredictResponse)
        async def predict(payload: PredictRequest):
            try:
                data = await self.news_api_service.get_news(
                    stock_symbol=payload.stock_symbol
                )

                if data is None:
                    return PredictResponse(
                        data=[],
                        message="No news found for this stock symbol."
                    )
                
                filtered_data = safe_get(data, "data")

                formatted_data = self.news_api_service.format_news(filtered_data)
                print(f"Found {len(formatted_data)} news articles")

                # Run FinBERT prediction on each headline
                result = []

                for headline_data in formatted_data:
                    headline_text = headline_data.get("text", "")
                    if not headline_text:
                        continue
                    
                    prediction_result = self.model.predict(headline_text)
                    prediction_result["source"] = headline_data.get("source", None)

                    result.append(prediction_result)
                
                return PredictResponse(
                    data=result,
                    message="Success"
                )
            except Exception as e:
                print(f"Predict route error : {str(e)}")
                return PredictResponse(
                    data=[],
                    message=f"Error : {str(e)}"
                )