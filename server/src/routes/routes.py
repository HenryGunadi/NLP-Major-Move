from fastapi import APIRouter
from schemas import PredictResponse, PredictRequest
from classes import NewsAPI, MachineLearningModel
from utils import safe_get

class MainRoute():
    def __init__(self, news_api_service: NewsAPI, model_service: MachineLearningModel):
        self.router = APIRouter()
        self.news_api_service = news_api_service
        self.model_service = model_service
    
        @self.router.post("/predict", response_model=PredictResponse)
        async def predict(payload: PredictRequest):
            try:
                data = await self.news_api_service.get_news(
                    stock_symbol=payload.stock_symbol
                )

                if data is None:
                    return PredictResponse(
                        data=[],
                        message="No news is found."
                    )
                
                filtered_data = safe_get(data, "data")
                # print("Filtered data : ", filtered_data)

                formatted_data = self.news_api_service.format_news(filtered_data)
                print("Formatted data : ", formatted_data)

                # do model prediction here
                prediction_result = model_service.predict(formatted_data)

                return PredictResponse(
                    data=data,
                    message="Success"
                )
            except Exception as e:
                print(f"Predict route error : {str(e)}")
                return PredictResponse(
                    data=[],
                    message=f"Error : {str(e)}"
                )