from celery import Celery
from app.core.config import setting

celery_app=Celery(
    "smart_support",
    broker=setting.REDIS_URL,
    backend=setting.REDIS_URL,
    include=["app.jobs.tasks"], 
)

celery_app.conf.update(
    task_routes={"app.jobs.tasks.*": {"queue": "classification"}},
    result_expires=3600,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    broker_connection_retry_on_startup=True,
)