from fastapi import FastAPI
from api.router import router

app = FastAPI(
	title="Capstone KPI & ML API",
	description="Backend API for KPI dashboard and ML predictions",
	version="1.0.0"
)

app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "App is running"}

if __name__ == "__main__":
	import uvicorn
	uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
