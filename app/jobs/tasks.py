from app.core.celery_app import celery_app
from app.services.triage import classify_ticket
from app.core.db import tickets_collection
from app.core.utils import run_async
import asyncio, re
from bson import ObjectId

@celery_app.task(bind=True, 
                 autoretry_for=(Exception,), 
                 retry_backoff=True, 
                 max_retries=3)
def classify_ticket_task(self, text:str):
  
    result=run_async(classify_ticket(text))
    
    ticket = {
        "text": text,
        "classification": result.get("classification"),
        "status": "classified"
    }
    ticket_id= run_async(tickets_collection.insert_one(ticket))

    summarize_ticket_task.apply_async((str(ticket_id.inserted_id), text), queue="enrichment")
    return {"ticket_id": str(ticket_id.inserted_id), "classification": result}


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def summarize_ticket_task(self, ticket_id: str, text: str):
    summary = f"Summary: {text[:75]}..."
    run_async(tickets_collection.update_one(
        {"_id": ObjectId(ticket_id)},
        {"$set": {"summary": summary, "status": "summarized"}}
    ))

    detect_pii_task.apply_async((ticket_id, text), queue="enrichment")
    return {"summary": summary}


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def detect_pii_task(self, ticket_id: str, text: str):
    email_found = bool(re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}", text))
    phone_found = bool(re.search(r"\b\d{10}\b", text))

    pii_data = {"email_detected": email_found, "phone_detected": phone_found}

    run_async(tickets_collection.update_one(
        {"_id": ObjectId(ticket_id)},
        {"$set": {"pii": pii_data, "status": "completed"}}
    ))
    return pii_data