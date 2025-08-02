from fastapi import APIRouter
from app.core.db import tickets_collection

router = APIRouter()

@router.get("/history")
async def get_ticket_history(limit: int = 10):
    cursor = tickets_collection.find().sort("_id", -1).limit(limit)
    tickets = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        tickets.append(doc)
    return {"tickets": tickets}
