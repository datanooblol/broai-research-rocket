from celery import Celery

def make_celery():
    celery_app = Celery(
        "broai",  # Name of your project
        broker="redis://localhost:6379/0",  # Celery broker URL (Redis in this case)
        backend="redis://localhost:6379/0",  # Celery result backend URL (Redis in this case)
        result_persistent=True,  # Make sure results are persistent
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        result_expires=60*5,  # Optional: expiry time for results (1 hour)
    )
    return celery_app

# This will be the shared Celery instance
celery_app = make_celery()

from . import scrape_worker
