from celery import Celery

def make_celery():
    celery_app = Celery(
        "broai",  # Name of your project
        broker="redis://localhost:6379/0",  # Celery broker URL (Redis in this case)
        backend="redis://localhost:6379/0",  # Celery result backend URL (Redis in this case)
    )
    return celery_app

# This will be the shared Celery instance
celery_app = make_celery()

from celery_workers import tasks, agents_demo
