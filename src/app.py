from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from services.model_service import model_service
from services.encoder_service import EncoderService
from services.predictor_service import PredictorService
from services.kpi_service import KPIService
from api import router
from api import kpi_router
from core.database import db
from core.logging import logger
from datetime import datetime
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up the application...")
    try:
        # Test database connection
        logger.info(
            "Testing database connection... using port "
            + str(db.config["port"])
            + " host "
            + str(db.config["host"])
        )
        db.test_connection()
    except:
        logger.exception("Database connection failed during startup")
        raise
    else:
        logger.success("Database connection successful.")

    logger.info("Loading models...")
    try:
        model_service.load_models()
    except:
        logger.exception("Failed to load models during startup")
        raise
    else:
        logger.success("Models loaded successfully.")

    # Initialize services after models loaded
    logger.info("Initializing services...")
    encoder_service = EncoderService()
    predictor_service = PredictorService()
    kpi_service = KPIService(cache_ttl_seconds=settings.KPI_CACHE_TTL_SECONDS)
    logger.success(f"Services initialized. KPI cache TTL: {settings.KPI_CACHE_TTL_SECONDS}s")

    import api.router as router_module

    app.state.model_service = model_service
    app.state.encoder_service = encoder_service
    app.state.predictor_service = predictor_service
    app.state.kpi_service = kpi_service
    logger.success("All services registered to app state.")

    yield

    # Shutdown
    logger.info("Shutting down the application...")


app = FastAPI(
    title="Capstone KPI & ML API",
    description="Backend API for KPI dashboard and ML predictions",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
