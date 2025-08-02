from fastapi import FastAPI
from app.api import classify, result, history

app = FastAPI(title="Smart Support System")

app.include_router(classify.router, prefix="/api")
app.include_router(result.router, prefix="/api")
app.include_router(history.router, prefix="/api")

@app.get("/")
def health_check():
    return {"status": "running"}
