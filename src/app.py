from fastapi import FastAPI
from contextlib import asynccontextmanager
from services import ModelService, PredictorService


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup
    # load models
    
    yield
    # Shutdown

app = FastAPI(
    title="Capstone KPI & ML API",
    description="Backend API for KPI dashboard and ML predictions",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "App is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
