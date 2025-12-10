from fastapi import FastAPI
from contextlib import asynccontextmanager
from services import ModelService, PredictorService
from core.logging import logger

model_service = ModelService()
predictor_service = PredictorService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up the application...")
    logger.info("loading models...")
    model_service.load_models()
    logger.success("Models loaded successfully.")    
    yield
    # Shutdown
    logger.info("Shutting down the application...")

app = FastAPI(
    title="Capstone KPI & ML API",
    description="Backend API for KPI dashboard and ML predictions",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "App is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
