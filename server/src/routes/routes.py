from fastapi import APIRouter
from schemas import PredictResponse, PredictRequest, SetModelRequest
from classes import NewsAPI, ModelManager
from utils import safe_get

class MainRoute():
    def __init__(self, news_api_service: NewsAPI, model_manager: ModelManager):
        self.router = APIRouter()
        self.news_api_service = news_api_service
        self.model_manager = model_manager
    
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

                # do model prediction on the news
                result = []

                for headline in formatted_data:
                    prediction_result = model_manager.predict(headline.get("headline", ""))
                    prediction_result["source"] = headline.get("source", None)

                    print("Prediction result : ", prediction_result)

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

        @self.router.post("/set_model")
        async def set_model(payload: SetModelRequest):
            try:
                model_manager.set_model(
                    model_name=payload.model_name
                )
                
                return {"message": "Success"}
            except Exception as e:
                print(f"Predict route error : {str(e)}")
                return {"message": f"Error : {str(e)}"}