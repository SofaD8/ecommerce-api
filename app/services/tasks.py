from app.core.celery_app import celery


@celery.task
def test_task():
    return "Celery is working!"
