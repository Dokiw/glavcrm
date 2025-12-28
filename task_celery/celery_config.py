from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

celery = Celery(
    "outbox",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["task_celery.publisher.task", "task_celery.handlers.task"],
)

celery.conf.update(
    timezone="Europe/Moscow",
    enable_utc=False,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)

# Celery Beat schedule: каждые N секунд
celery.conf.beat_schedule = {
    "check-outbox-every-10-seconds": {
        "task": "task_celery.publisher.task.process_outbox",
        "schedule": 10.0,  # каждые 10 секунд
        "options": {"queue": "outbox"},
    },
}