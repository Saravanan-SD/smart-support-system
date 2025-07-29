from fastapi import APIRouter
from app.core.celery_app import celery_app

router =APIRouter()

@router.get("/result/{task_id}")
async def get_result(task_id:str):

    result =celery_app.AsyncResult(task_id)

    if result.ready():
        return {"status": "completed","result": result.result}
    return {"status": result.status}