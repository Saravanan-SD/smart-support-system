from fastapi import APIRouter, Body
from app.jobs.tasks import classify_ticket_task

router =APIRouter()

@router.post("/classify")
async def classify(text:str =Body(...,embed=True)):
    """
    Classify a support ticket by category and priority.
    """
    task= classify_ticket_task.delay(text)
    return {"job_id":task.id, "status":"queued"}