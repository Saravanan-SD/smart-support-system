from fastapi import FastAPI
from app.api import classify

app = FastAPI(title="Smart Support System")

app.include_router(classify.router)

@app.get("/")
def health_check():
    return {"status": "running"}