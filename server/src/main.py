from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import MainRoute
from classes import NewsAPI, FinBERT
import uvicorn
from config import config
from pathlib import Path

# Get base directory
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "finbert"

# Services
news_api_service = NewsAPI(
    api_key=config.get_news_api_token,
    base_url=config.NEWS_API_BASE_URL
)

# Initialize FinBERT model
print("Initializing FinBERT model...")
finbert_model = FinBERT(model_path=MODEL_PATH)
print("FinBERT model loaded successfully!")

# Routers
main_router = MainRoute(
    news_api_service=news_api_service,
    model=finbert_model
)

app = FastAPI(title="MajorMove - Stock News Analysis")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:5500",
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
    return {"message": "MajorMove API is running with FinBERT model!"}

if __name__ == "__main__":
    port = 8000
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=False)