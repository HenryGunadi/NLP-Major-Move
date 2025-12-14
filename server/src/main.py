from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import MainRoute
from classes import NewsAPI, ModelManager, NaiveBayes, MLogistic, RandomForest
import uvicorn
from config import config

# services
news_api_service = NewsAPI(
   api_key=config.get_news_api_token,
   base_url=config.NEWS_API_BASE_URL
)

# model manager (set default model)
model_manager = ModelManager() 

# default model
# model_manager.set_model("mlogistic")

# routers
main_router = MainRoute(
   news_api_service=news_api_service,
   model_manager=model_manager
)

app = FastAPI(title="Basic FastAPI Setup")

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(main_router.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "FastAPI is running!"}

if __name__ == "__main__":
  port = 8000
  uvicorn.run("main:app", host="127.0.0.1", port=port, reload=False)