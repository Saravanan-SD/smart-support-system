from app.core.celery_app import celery_app
from app.services.triage import classify_ticket

@celery_app.task(bind=True, 
                 autoretry_for=(Exception,), 
                 retry_backoff=True, 
                 max_retries=3)
def classify_ticket_task(self, text:str):

    import asyncio
    result=asyncio.run(classify_ticket(text))
    return result