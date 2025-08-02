from celery import Celery
from app.core.config import setting

celery_app=Celery(
    "smart_support",
    broker=setting.REDIS_URL,
    backend=setting.REDIS_URL,
    include=["app.jobs.tasks"], 
)

celery_app.conf.update(
    task_routes={"app.jobs.tasks.classify_ticket_task": {"queue": "classification"},
                "app.jobs.tasks.summarize_ticket_task": {"queue": "enrichment"},
                "app.jobs.tasks.detect_pii_task": {"queue": "enrichment"},
    },
    task_default_retry_delay=5,
    task_time_limit=60,
    task_acks_late=True,
    broker_connection_retry_on_startup=True,
)

