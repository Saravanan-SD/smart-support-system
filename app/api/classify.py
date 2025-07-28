from fastapi import APIRouter, Body
from app.services.triage import classify_ticket

router =APIRouter()

@router.post("/classify")
async def classify(text:str =Body(...,embed=True)):
    """
    Classify a support ticket by category and priority.
    """
    return await classify_ticket(text)