from task_celery.celery_config import celery


@celery.task(name="task.process_outbox", bind=True, acks_late=True)
def process_outbox():
    """
    Читает pending-события из Outbox
    и отправляет их в Celery workers.
    """
