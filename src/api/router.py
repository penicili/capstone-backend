from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
	return {"message": "API Route is working"}

@router.post("/predict")
async def predict(data: dict):
	return {"message": "Prediction successful", "data": data}

