from app.core.celery_app import celery_app

import app.jobs.tasks

__all__ =("celery_app",)