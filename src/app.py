from fastapi import FastAPI
from contextlib import asynccontextmanager
from services.model_service import model_service
from services.encoder_service import encoder_service
from services.predictor_service import predictor_service
from services.kpi_service import kpi_service
from api import router
from api import kpi_router
from core.database import db
from core.logging import logger
from datetime import datetime

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up the application...")
    
    # Test database connection
    logger.info("Testing database connection... using port "+str(db.config['port']) + " host "+ str(db.config['host']))
    if db.test_connection():
        logger.success("Database connection successful")
    else:
        logger.error("Database connection failed")
    
    logger.info("Loading models...")
    model_service.load_models()
    logger.success("Models loaded successfully.")
    
    # Initialize services after models loaded
    logger.info("Initializing services...")
    import api.router as router_module
    app.state.model_service = model_service
    app.state.encoder_service = encoder_service
    app.state.predictor_service = predictor_service
    app.state.kpi_service = kpi_service
    logger.success("Services initialized successfully.")
    
    yield
    
    # Shutdown
    logger.info("Shutting down the application...")

app = FastAPI(
    title="Capstone KPI & ML API",
    description="Backend API for KPI dashboard and ML predictions",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(router)
app.include_router(kpi_router)

@app.get("/")
async def root():
    return {"message": "Capstone API is running"}

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "models_ready": model_service.is_ready(),
        "database_connected": db.test_connection(),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
