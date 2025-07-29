from fastapi import FastAPI
from app.api import classify
from app.api import result

app = FastAPI(title="Smart Support System")

app.include_router(classify.router)
app.include_router(result.router)

@app.get("/")
def health_check():
    return {"status": "running"}