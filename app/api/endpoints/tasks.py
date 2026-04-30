from fastapi import APIRouter

from app.services.tasks import test_task


router = APIRouter()


@router.post("/test-task")
def run_test_task():
    task = test_task.delay()
    return {"Status": "send_task", "task_id": task.id}
